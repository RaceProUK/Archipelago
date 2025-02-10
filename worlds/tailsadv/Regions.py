from enum import Enum
from typing import Dict, List, NamedTuple

TailsAdvRegion = Enum("Region", [
    ("Menu", "Menu"),
    ("PoloyForest", "Poloy Forest"),
    ("VolcanicTunnel", "Volcanic Tunnel"),
    ("PollyMountain1", "Polly Mountain 1"),
    ("LakeRocky", "Lake Rocky"),
    ("CavernIsland", "Cavern Island"),
    ("GreenIsland", "Green Island"),
    ("CaronForest", "Caron Forest"),
    ("LakeCrystal", "Lake Crystal"),
    ("PollyMountain2", "Polly Mountain 2"),
    ("CocoIsland", "Coco Island"),
    ("BattleFortress1", "Battle Fortress 1"),
    ("BattleFortress2", "Battle Fortress 2")
])

class TailsAdvRegionData(NamedTuple):
    connecting_regions: List[TailsAdvRegion] = []

region_data_table: Dict[TailsAdvRegion, TailsAdvRegionData] = {
    TailsAdvRegion.Menu: TailsAdvRegionData([TailsAdvRegion.PoloyForest,
                                             TailsAdvRegion.LakeRocky]),
    TailsAdvRegion.PoloyForest: TailsAdvRegionData([TailsAdvRegion.VolcanicTunnel]),
    TailsAdvRegion.VolcanicTunnel: TailsAdvRegionData([TailsAdvRegion.PollyMountain1]),
    TailsAdvRegion.PollyMountain1: TailsAdvRegionData([]),
    TailsAdvRegion.LakeRocky: TailsAdvRegionData([TailsAdvRegion.CavernIsland,
                                                  TailsAdvRegion.GreenIsland,
                                                  TailsAdvRegion.CaronForest,
                                                  TailsAdvRegion.LakeCrystal,
                                                  TailsAdvRegion.CocoIsland]),
    TailsAdvRegion.CavernIsland: TailsAdvRegionData([]),
    TailsAdvRegion.GreenIsland: TailsAdvRegionData([]),
    TailsAdvRegion.CaronForest: TailsAdvRegionData([]),
    TailsAdvRegion.LakeCrystal: TailsAdvRegionData([TailsAdvRegion.PollyMountain2]),
    TailsAdvRegion.PollyMountain2: TailsAdvRegionData([]),
    TailsAdvRegion.CocoIsland: TailsAdvRegionData([TailsAdvRegion.BattleFortress1]),
    TailsAdvRegion.BattleFortress1: TailsAdvRegionData([TailsAdvRegion.BattleFortress2]),
    TailsAdvRegion.BattleFortress2: TailsAdvRegionData([])
}