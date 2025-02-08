from typing import Dict, NamedTuple

from BaseClasses import Item, ItemClassification

class TailsAdvItem(Item):
    game = "Tails Adventure"

class TailsAdvItemData(NamedTuple):
    code: int
    type: ItemClassification
    can_create: bool = True
    start_with: bool = False

item_data_table: Dict[str, TailsAdvItemData] = {
    "Regular Bomb": TailsAdvItemData(1, ItemClassification.progression, can_create=False, start_with=True),
    "Large Bomb": TailsAdvItemData(2, ItemClassification.progression),
    "Remote Bomb": TailsAdvItemData(3, ItemClassification.progression),
    "Napalm Bomb": TailsAdvItemData(4, ItemClassification.progression),
    "Triple Bomb": TailsAdvItemData(5, ItemClassification.useful),
    "Wrench": TailsAdvItemData(6, ItemClassification.useful),
    "Helmet": TailsAdvItemData(7, ItemClassification.useful),
    "Item Radar": TailsAdvItemData(8, ItemClassification.useful),
    "Radio": TailsAdvItemData(9, ItemClassification.useful),
    "Hammer": TailsAdvItemData(10, ItemClassification.useful),
    "Teleport Device": TailsAdvItemData(11, ItemClassification.useful),
    "Night Vision": TailsAdvItemData(12, ItemClassification.progression),
    "Speed Boots": TailsAdvItemData(13, ItemClassification.useful),
    "Super Glove": TailsAdvItemData(14, ItemClassification.useful),
    "Fang": TailsAdvItemData(15, ItemClassification.useful),
    "Knuckles": TailsAdvItemData(16, ItemClassification.useful),
    "Sonic": TailsAdvItemData(17, ItemClassification.useful),
    "Proton Torpedo": TailsAdvItemData(18, ItemClassification.progression),
    "Vulcan Gun": TailsAdvItemData(19, ItemClassification.progression, can_create=False, start_with=True),
    "Extra Speed": TailsAdvItemData(20, ItemClassification.progression),
    "Extra Armor": TailsAdvItemData(21, ItemClassification.progression),
    "Anti Air Missile": TailsAdvItemData(22, ItemClassification.progression),
    "Spark": TailsAdvItemData(23, ItemClassification.useful),
    "Mine": TailsAdvItemData(24, ItemClassification.useful),
    "Rocket Booster": TailsAdvItemData(25, ItemClassification.progression),
    "Remote Robot": TailsAdvItemData(26, ItemClassification.progression),
    "Blue Chaos Emerald": TailsAdvItemData(27, ItemClassification.useful),
    "Green Chaos Emerald": TailsAdvItemData(28, ItemClassification.useful),
    "Purple Chaos Emerald": TailsAdvItemData(29, ItemClassification.useful),
    "Red Chaos Emerald": TailsAdvItemData(30, ItemClassification.useful),
    "White Chaos Emerald": TailsAdvItemData(31, ItemClassification.useful),
    "Yellow Chaos Emerald": TailsAdvItemData(32, ItemClassification.useful),
    "Ring": TailsAdvItemData(33, ItemClassification.filler, can_create=False)
}

item_table = {
    name: data.code for name, data in item_data_table.items()
}