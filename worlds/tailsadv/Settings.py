import settings

from .ROM import ROMType

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