from dataclasses import dataclass
from typing import List

from Options import Range, Toggle, OptionGroup, ProgressionBalancing, Accessibility, PerGameCommonOptions, StartInventoryPool

class RequiredChaosEmeraldCount(Range):
    """How many Chaos Emeralds must be collected to reach the goal"""
    display_name = "Chaos Emeralds Required"
    range_start = 0
    range_end = 6
    default = 6

class RequireNightVision(Toggle):
    """Whether Night Vision is required for Polly Mountain 2"""
    display_name = "Require Night Vision"
    default = True

@dataclass
class TailsAdvOptions(PerGameCommonOptions):
    required_emerald_count: RequiredChaosEmeraldCount
    require_nvg: RequireNightVision
    start_inventory_from_pool: StartInventoryPool

tailsadv_option_groups: List[OptionGroup] = [
    OptionGroup("Customization", [
        RequiredChaosEmeraldCount,
        RequireNightVision,
    ]),
    OptionGroup("Advanced Options", [
        ProgressionBalancing,
        Accessibility,
    ]),
]