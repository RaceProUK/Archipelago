from typing import Dict, NamedTuple

from BaseClasses import Location
from .Regions import TailsAdvRegion

class TailsAdvLocation(Location):
    game = "Tails Adventure"

class TailsAdvLocationData(NamedTuple):
    code: int
    region: TailsAdvRegion
    can_create: bool = True

location_data_table: Dict[str, TailsAdvLocationData] = {
    "Regular Bomb": TailsAdvLocationData(1, TailsAdvRegion.Menu, can_create=False),
    "Large Bomb": TailsAdvLocationData(2, TailsAdvRegion.PollyMountain2),
    "Remote Bomb": TailsAdvLocationData(3, TailsAdvRegion.VolcanicTunnel),
    "Napalm Bomb": TailsAdvLocationData(4, TailsAdvRegion.CavernIsland),
    "Triple Bomb": TailsAdvLocationData(5, TailsAdvRegion.CaronForest),
    "Wrench": TailsAdvLocationData(6, TailsAdvRegion.BattleFortress2),
    "Helmet": TailsAdvLocationData(7, TailsAdvRegion.PollyMountain1),
    "Item Radar": TailsAdvLocationData(8, TailsAdvRegion.PollyMountain2),
    "Radio": TailsAdvLocationData(9, TailsAdvRegion.PoloyForest),
    "Hammer": TailsAdvLocationData(10, TailsAdvRegion.VolcanicTunnel),
    "Teleport Device": TailsAdvLocationData(11, TailsAdvRegion.CocoIsland),
    "Night Vision": TailsAdvLocationData(12, TailsAdvRegion.GreenIsland),
    "Speed Boots": TailsAdvLocationData(13, TailsAdvRegion.PoloyForest),
    "Super Glove": TailsAdvLocationData(14, TailsAdvRegion.PollyMountain1),
    "Fang": TailsAdvLocationData(15, TailsAdvRegion.PollyMountain2),
    "Knuckles": TailsAdvLocationData(16, TailsAdvRegion.PollyMountain1),
    "Sonic": TailsAdvLocationData(17, TailsAdvRegion.CaronForest),
    "Proton Torpedo": TailsAdvLocationData(18, TailsAdvRegion.CaronForest),
    "Vulcan Gun": TailsAdvLocationData(19, TailsAdvRegion.Menu, can_create=False),
    "Extra Speed": TailsAdvLocationData(20, TailsAdvRegion.GreenIsland),
    "Extra Armor": TailsAdvLocationData(21, TailsAdvRegion.VolcanicTunnel),
    "Anti Air Missile": TailsAdvLocationData(22, TailsAdvRegion.CavernIsland),
    "Spark": TailsAdvLocationData(23, TailsAdvRegion.PoloyForest),
    "Mine": TailsAdvLocationData(24, TailsAdvRegion.CavernIsland),
    "Rocket Booster": TailsAdvLocationData(25, TailsAdvRegion.PollyMountain1),
    "Remote Robot": TailsAdvLocationData(26, TailsAdvRegion.PoloyForest),
    "Blue Chaos Emerald": TailsAdvLocationData(27, TailsAdvRegion.CaronForest),
    "Green Chaos Emerald": TailsAdvLocationData(28, TailsAdvRegion.VolcanicTunnel),
    "Purple Chaos Emerald": TailsAdvLocationData(29, TailsAdvRegion.PollyMountain1),
    "Red Chaos Emerald": TailsAdvLocationData(30, TailsAdvRegion.PoloyForest),
    "White Chaos Emerald": TailsAdvLocationData(31, TailsAdvRegion.GreenIsland),
    "Yellow Chaos Emerald": TailsAdvLocationData(32, TailsAdvRegion.CocoIsland)
}

location_table = {
    name: data.code for name, data in location_data_table.items()
}

location_groups = {
    "Poloy Forest": { "Red Chaos Emerald", "Radio", "Remote Robot", "Spark", "Speed Boots" },
    "Volcanic Tunnel": { "Extra Armor", "Green Chaos Emerald", "Hammer", "Remote Bomb" },
    "Polly Mountain 1": { "Helmet", "Knuckles", "Purple Chaos Emerald", "Super Glove", "Rocket Booster" },
    "Lake Rocky": {},
    "Cavern Island": { "Anti Air Missile", "Mine", "Napalm Bomb" },
    "Green Island": { "Extra Speed", "Night Vision", "White Chaos Emerald" },
    "Caron Forest": { "Blue Chaos Emerald", "Proton Torpedo", "Sonic", "Triple Bomb" },
    "Lake Crystal": {},
    "Polly Mountain 2": { "Fang", "Item Radar", "Large Bomb" },
    "Coco Island": { "Teleport Device", "Yellow Chaos Emerald" },
    "Battle Fortress 1": {},
    "Battle Fortress 2": { "Wrench" }
}