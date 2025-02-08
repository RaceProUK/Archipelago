from dataclasses import dataclass
from Options import Toggle, PerGameCommonOptions, StartInventoryPool

class RequireNightVision(Toggle):
    """Whether the Night Vision Googles are required for Polly Mountain 2"""
    display_name = "Require Night Vision for Polly Mountain 2"

@dataclass
class TailsAdvOptions(PerGameCommonOptions):
    require_nvg: RequireNightVision
    start_inventory_from_pool: StartInventoryPool