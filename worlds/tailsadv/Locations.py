from typing import Dict, NamedTuple

from BaseClasses import Location

class TailsAdvLocation(Location):
    game = "Tails Adventure"

class TailsAdvLocationData(NamedTuple):
    code: int
    can_create: bool = True

location_data_table: Dict[str, TailsAdvLocationData] = {
    "Regular Bomb": TailsAdvLocationData(1, can_create=False),
    "Large Bomb": TailsAdvLocationData(2),
    "Remote Bomb": TailsAdvLocationData(3),
    "Napalm Bomb": TailsAdvLocationData(4),
    "Triple Bomb": TailsAdvLocationData(5),
    "Wrench": TailsAdvLocationData(6),
    "Helmet": TailsAdvLocationData(7),
    "Item Radar": TailsAdvLocationData(8),
    "Radio": TailsAdvLocationData(9),
    "Hammer": TailsAdvLocationData(10),
    "Teleport Device": TailsAdvLocationData(11),
    "Night Vision": TailsAdvLocationData(12),
    "Speed Boots": TailsAdvLocationData(13),
    "Super Glove": TailsAdvLocationData(14),
    "Fang": TailsAdvLocationData(15),
    "Knuckles": TailsAdvLocationData(16),
    "Sonic": TailsAdvLocationData(17),
    "Proton Torpedo": TailsAdvLocationData(18),
    "Vulcan Gun": TailsAdvLocationData(19, can_create=False),
    "Extra Speed": TailsAdvLocationData(20),
    "Extra Armor": TailsAdvLocationData(21),
    "Anti Air Missile": TailsAdvLocationData(22),
    "Spark": TailsAdvLocationData(23),
    "Mine": TailsAdvLocationData(24),
    "Rocket Booster": TailsAdvLocationData(25),
    "Remote Robot": TailsAdvLocationData(26),
    "Blue Chaos Emerald": TailsAdvLocationData(27),
    "Green Chaos Emerald": TailsAdvLocationData(28),
    "Purple Chaos Emerald": TailsAdvLocationData(29),
    "Red Chaos Emerald": TailsAdvLocationData(30),
    "White Chaos Emerald": TailsAdvLocationData(31),
    "Yellow Chaos Emerald": TailsAdvLocationData(32)
}

location_table = {
    name: data.code for name, data in location_data_table.items()
}