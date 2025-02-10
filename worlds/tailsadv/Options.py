from dataclasses import dataclass
from typing import List

from Options import Toggle, OptionGroup, ProgressionBalancing, Accessibility, PerGameCommonOptions, StartInventoryPool

class RequireNightVision(Toggle):
    """Whether Night Vision is required for Polly Mountain 2"""
    display_name = "Require Night Vision"
    default = True

@dataclass
class TailsAdvOptions(PerGameCommonOptions):
    require_nvg: RequireNightVision
    start_inventory_from_pool: StartInventoryPool

tailsadv_option_groups: List[OptionGroup] = [
    OptionGroup("Customization", [
        RequireNightVision,
    ]),
    OptionGroup("Advanced Options", [
        ProgressionBalancing,
        Accessibility,
    ]),
]