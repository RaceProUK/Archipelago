import settings
import typing

from typing import List

from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

from .Items import TailsAdvItem, item_data_table, item_table
from .Locations import TailsAdvLocation, location_data_table, location_table
from .Options import TailsAdvOptions, tailsadv_option_groups
from .Regions import region_data_table
from .Rules import set_rules
from .ROM import generate_output

class TailsAdvSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Tails Adventure ROM"""
        description = "Tails Adventure ROM File"
        copy_to = "Tails Adventure (U).gg"
        md5_cartridge = "a8bdb1beed088ff83c725c5af6b85e1f"
        md5_vc = "c2fe111a6e569ec6d58b9ecc32de0e12"
        md5s = [md5_cartridge, md5_vc]
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
    settings: typing.ClassVar[TailsAdvSettings]
    options: TailsAdvOptions
    options_dataclass = TailsAdvOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> TailsAdvItem:
        return TailsAdvItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
    
    def create_items(self) -> None:
        item_pool: List[TailsAdvItem] = []

        for name, item in item_data_table.items():
            # Add normal items to pool
            if item.can_create:
                item_pool.append(self.create_item(name))
            
            # Push pre-collected items
            if item.start_with:
                self.multiworld.push_precollected(self.create_item(name))

        self.multiworld.itempool += item_pool
    
    def create_regions(self) -> None:
        # Create regions
        for region_key in region_data_table.keys():
            region = Region(region_key.name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations
        for region_key, region_data in region_data_table.items():
            region = self.get_region(region_key.name)
            region.add_locations({
                location_name: location_data.code
                  for location_name, location_data
                  in location_data_table.items()
                  if location_data.can_create and location_data.region == region_key
            }, TailsAdvLocation)
            region.add_exits(list(region.name for region in region_data.connecting_regions))
    
    def get_filler_item_name(self) -> str:
        filler_items = list(name
                             for name, data
                             in item_data_table.items()
                             if data.type == ItemClassification.filler)
        return self.multiworld.random.choice(filler_items)
    
    def set_rules(self):
        set_rules(self.player, self.multiworld, self.options)
    
    def generate_output(self, output_directory):
        generate_output(self, output_directory)