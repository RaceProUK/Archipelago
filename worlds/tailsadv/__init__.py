import os
import settings
import typing

from typing import List

from BaseClasses import Item, ItemClassification, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

from .Items import TailsAdvItem, item_data_table, item_table, item_groups
from .Locations import TailsAdvLocation, location_data_table, location_table, location_groups
from .Options import TailsAdvOptions, tailsadv_option_groups
from .Regions import region_data_table
from .Rules import set_rules
from .ROM import ROMType, TailsAdvPatch
from . import Client

class TailsAdvSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Tails Adventure ROM"""
        description = "Tails Adventure ROM File"
        copy_to = "Tails Adventure (U).gg"
        md5s = [
            ROMType.Original.value,
            ROMType.VC3DS.value,
            ROMType.Origins.value
        ]
    rom_file: RomFile = RomFile(RomFile.copy_to)

class TailsAdvWebWorld(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to setting up the Tails Adventure randomizer connected to an Archipelago Multiworld.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["RaceProUK"]
    )
    tutorials = [setup_en]
    option_groups = tailsadv_option_groups

class TailsAdvWorld(World):
    """Tails Adventure (テイルスアドベンチャー) is a mini-Metroidvania starring Miles 'Tails' Prower, released in 1995 for the Sega Game Gear"""
    game = "Tails Adventure"
    web = TailsAdvWebWorld()
    settings: typing.ClassVar[TailsAdvSettings] # type: ignore
    options: TailsAdvOptions # type: ignore
    options_dataclass = TailsAdvOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    location_name_groups = location_groups
    item_name_groups = item_groups

    def create_item(self, name: str) -> TailsAdvItem:
        return TailsAdvItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
    
    def create_items(self) -> None:
        item_pool: List[Item|TailsAdvItem] = []

        # Add all placeable items and push precollected items
        for name, item in item_data_table.items():
            if item.start_with:
                self.multiworld.push_precollected(self.create_item(name))
            elif item.singleton and name not in self.options.start_inventory:
                item_pool.append(self.create_item(name))
        
        # Add required filler
        location_count = len({location_data for location_data in location_data_table.values() if location_data.can_create})
        item_count = len(item_pool)
        item_pool += [self.create_filler() for _ in range(item_count, location_count)]

        self.multiworld.itempool += item_pool
    
    def create_regions(self) -> None:
        # Create regions
        for region_key in region_data_table.keys():
            region = Region(region_key.name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Add locations to regions and connect the latter
        for region_key, region_data in region_data_table.items():
            region = self.get_region(region_key.name)
            region.add_locations({
                location_name: location_data.code
                for location_name, location_data
                in location_data_table.items()
                if location_data.can_create and location_data.region == region_key
            }, TailsAdvLocation)
            region.add_exits([region.name for region in region_data.connecting_regions])
    
    def get_filler_item_name(self) -> str:
        filler_items = [name
                        for name, data
                        in item_data_table.items()
                        if data.type == ItemClassification.filler and not data.singleton]
        return self.multiworld.random.choice(filler_items)
    
    def set_rules(self) -> None:
        set_rules(self.player, self.multiworld, self.options)
    
    def generate_output(self, output_directory) -> None:
        patch = TailsAdvPatch(player = self.player, player_name = self.player_name)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))