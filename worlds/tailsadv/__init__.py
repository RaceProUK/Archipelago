from typing import List

from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

from .Items import TailsAdvItem, item_data_table, item_table
from .Locations import location_data_table, location_table
from .Options import TailsAdvOptions, tailsadv_option_groups

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
        # Create regions (TODO: define regions)
        region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(region)

        # Create locations
        region.add_locations({
            name: data.code for name, data in location_data_table.items() if data.can_create
        })
    
    def get_filler_item_name(self) -> str:
        filler_items = list(name for name, data in item_data_table.items() if data.type == ItemClassification.filler)
        return self.multiworld.random.choice(filler_items)