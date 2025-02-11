from typing import Callable

from BaseClasses import MultiWorld, CollectionState
from worlds.generic.Rules import set_rule
from .Options import TailsAdvOptions

CollectionRule = Callable[[CollectionState], bool]

def set_rules(player: int, multiworld: MultiWorld, options: TailsAdvOptions) -> None:
    # Conditions
    has_remote_robot: CollectionRule = lambda state: state.has("Remote Robot", player)
    has_remote_bomb: CollectionRule = lambda state: state.has("Remote Bomb", player)
    has_large_bomb: CollectionRule = lambda state: state.has("Large Bomb", player)
    has_napalm_bomb: CollectionRule = lambda state: state.has("Napalm Bomb", player)
    has_anti_air: CollectionRule = lambda state: state.has("Anti Air Missile", player)
    has_extra_speed: CollectionRule = lambda state: state.has("Extra Speed", player)
    has_mine: CollectionRule = lambda state: state.has("Mine", player)
    has_extra_armor: CollectionRule = lambda state: state.has("Extra Armor", player)
    has_rocket_booster: CollectionRule = lambda state: state.has("Rocket Booster", player)
    has_night_vision: CollectionRule = lambda state: state.has("Night Vision", player)

    # Regions
    set_rule(multiworld.get_entrance("Menu -> LakeRocky", player), has_remote_robot)
    
    set_rule(multiworld.get_entrance("PoloyForest -> CaronForest", player),
             lambda state: has_remote_robot(state) and has_napalm_bomb(state))
    
    set_rule(multiworld.get_entrance("VolcanicTunnel -> PollyMountain1", player), has_remote_bomb)
    
    set_rule(multiworld.get_entrance("LakeRocky -> GreenIsland", player), has_anti_air)
    set_rule(multiworld.get_entrance("LakeRocky -> LakeCrystal", player), has_extra_speed)
    set_rule(multiworld.get_entrance("LakeRocky -> CocoIsland", player),
             lambda state: has_mine(state) and has_extra_armor(state))
    
    set_rule(multiworld.get_entrance("CocoIsland -> BattleFortress1", player), has_rocket_booster)

    set_rule(multiworld.get_entrance("BattleFortress1 -> BattleFortress2", player), has_remote_bomb)
    
    if options.require_nvg:
        set_rule(multiworld.get_entrance("LakeCrystal -> PollyMountain2", player), has_night_vision)
    
    # Locations
    set_rule(multiworld.get_location("Speed Boots", player), has_remote_robot)
    set_rule(multiworld.get_location("Radio", player), has_remote_robot)
    set_rule(multiworld.get_location("Remote Bomb", player), has_remote_robot)

    set_rule(multiworld.get_location("Green Chaos Emerald", player), has_remote_bomb)
    set_rule(multiworld.get_location("Napalm Bomb", player), has_remote_bomb)
    set_rule(multiworld.get_location("Anti Air Missile", player), has_remote_bomb)

    set_rule(multiworld.get_location("Rocket Booster", player), has_large_bomb)

    set_rule(multiworld.get_location("Spark", player), has_napalm_bomb)

    set_rule(multiworld.get_location("Extra Armor", player),
             lambda state: has_remote_bomb(state) and has_large_bomb(state))
    
    # Completion
    multiworld.completion_condition[player] = lambda state: state.can_reach("BattleFortress2", "Region", player)