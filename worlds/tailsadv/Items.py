from typing import Dict, NamedTuple

from BaseClasses import Item, ItemClassification

class TailsAdvItem(Item):
    game = "Tails Adventure"

class TailsAdvItemData(NamedTuple):
    code: int
    page: int
    bit: int
    type: ItemClassification
    can_create: bool = True
    start_with: bool = False

item_data_table: Dict[str, TailsAdvItemData] = {
    "Regular Bomb": TailsAdvItemData(1, 1, 7, ItemClassification.progression, can_create=False, start_with=True),
    "Large Bomb": TailsAdvItemData(2, 1, 6, ItemClassification.progression),
    "Remote Bomb": TailsAdvItemData(3, 1, 5, ItemClassification.progression),
    "Napalm Bomb": TailsAdvItemData(4, 1, 4, ItemClassification.progression),
    "Triple Bomb": TailsAdvItemData(5, 1 ,3, ItemClassification.useful),
    "Wrench": TailsAdvItemData(6, 1, 2, ItemClassification.useful),
    "Helmet": TailsAdvItemData(7, 1, 1, ItemClassification.useful),
    "Item Radar": TailsAdvItemData(8, 3, 7, ItemClassification.useful),
    "Radio": TailsAdvItemData(9, 3, 6, ItemClassification.useful),
    "Hammer": TailsAdvItemData(10, 2, 7, ItemClassification.useful),
    "Teleport Device": TailsAdvItemData(11, 2, 6, ItemClassification.useful),
    "Night Vision": TailsAdvItemData(12, 2, 5, ItemClassification.progression),
    "Speed Boots": TailsAdvItemData(13, 2, 4, ItemClassification.useful),
    "Super Glove": TailsAdvItemData(14, 2, 3, ItemClassification.useful),
    "Fang": TailsAdvItemData(15, 2, 2, ItemClassification.useful),
    "Knuckles": TailsAdvItemData(16, 2, 1, ItemClassification.useful),
    "Sonic": TailsAdvItemData(17, 2, 0, ItemClassification.useful),
    "Proton Torpedo": TailsAdvItemData(18, 4, 7, ItemClassification.progression),
    "Vulcan Gun": TailsAdvItemData(19, 4, 6, ItemClassification.progression, can_create=False, start_with=True),
    "Extra Speed": TailsAdvItemData(20, 4, 5, ItemClassification.progression),
    "Extra Armor": TailsAdvItemData(21, 4, 4, ItemClassification.progression),
    "Anti Air Missile": TailsAdvItemData(22, 4, 3, ItemClassification.progression),
    "Spark": TailsAdvItemData(23, 4, 2, ItemClassification.useful),
    "Mine": TailsAdvItemData(24, 4, 1, ItemClassification.progression),
    "Rocket Booster": TailsAdvItemData(25, 4, 0, ItemClassification.progression),
    "Remote Robot": TailsAdvItemData(26, 1, 0, ItemClassification.progression),
    "Blue Chaos Emerald": TailsAdvItemData(27, 3, 5, ItemClassification.useful),
    "Green Chaos Emerald": TailsAdvItemData(28, 3, 4, ItemClassification.useful),
    "Purple Chaos Emerald": TailsAdvItemData(29, 3, 3, ItemClassification.useful),
    "Red Chaos Emerald": TailsAdvItemData(30, 3, 2, ItemClassification.useful),
    "White Chaos Emerald": TailsAdvItemData(31, 3, 1, ItemClassification.useful),
    "Yellow Chaos Emerald": TailsAdvItemData(32, 3, 0, ItemClassification.useful),
    "Ring": TailsAdvItemData(33, 0, 0, ItemClassification.filler, can_create=False)
}

item_table = {
    name: data.code for name, data in item_data_table.items()
}