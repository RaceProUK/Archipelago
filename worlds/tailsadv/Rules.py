from BaseClasses import MultiWorld
from worlds.generic.Rules import set_rule
from .Options import TailsAdvOptions

def set_rules(player: int, multiworld: MultiWorld, options: TailsAdvOptions):
    # Conditions
    has_remote_robot = lambda state: state.has("Remote Robot", player, 1)
    has_remote_bomb = lambda state: state.has("Remote Bomb", player, 1)
    has_large_bomb = lambda state: state.has("Large Bomb", player, 1)
    has_napalm_bomb = lambda state: state.has("Napalm Bomb", player, 1)
    has_anti_air = lambda state: state.has("Anti Air Missile", player, 1)
    has_extra_speed = lambda state: state.has("Extra Speed", player, 1)
    has_mine = lambda state: state.has("Mine", player, 1)
    has_extra_armor = lambda state: state.has("Extra Armor", player, 1)
    has_rocket_booster = lambda state: state.has("Rocket Booster", player, 1)
    has_night_vision = lambda state: state.has("Night Vision", player, 1)

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
    set_rule(multiworld.get_location("Radio", player), has_remote_robot)
    set_rule(multiworld.get_location("Remote Bomb", player), has_remote_robot)

    set_rule(multiworld.get_location("Green Chaos Emerald", player), has_remote_bomb)
    set_rule(multiworld.get_location("Napalm Bomb", player), has_remote_bomb)
    set_rule(multiworld.get_location("Anti Air Missile", player), has_remote_bomb)

    set_rule(multiworld.get_location("Napalm Bomb", player),
             lambda state: has_remote_bomb(state) and has_large_bomb(state))