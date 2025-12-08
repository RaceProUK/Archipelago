import settings

from enum import Enum

ROMType = Enum("ROMType", [
    ("Original", "a8bdb1beed088ff83c725c5af6b85e1f"), # Also SADX and Gems
    ("VC3DS", "c2fe111a6e569ec6d58b9ecc32de0e12"),
    ("Origins", "9a2892a5c14b52d517ec74685365314f")
])

class TailsAdvSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Tails Adventure ROM"""
        description = "Tails Adventure ROM File"
        copy_to = "Tails Adventure (U).gg"
        md5s = [
            ROMType.Original.value,
            ROMType.VC3DS.value,
            ROMType.Origins.value
        ]
    rom_file: RomFile = RomFile(RomFile.copy_to)