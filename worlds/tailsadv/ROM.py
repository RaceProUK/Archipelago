import logging
import os
import hashlib
import bsdiff4
import pkgutil
import Utils

from typing import List

from worlds.Files import APProcedurePatch, APPatchExtension, InvalidDataError

from .Settings import TailsAdvSettings, ROMType
from . import Patches

logger = logging.getLogger("ROM")

class TailsAdvPatcher(APPatchExtension):
    game = "Tails Adventure"

    @staticmethod
    def apply_tailsadv_patch(caller: APProcedurePatch, rom: bytes) -> bytes:
        md5 = hashlib.md5(rom).hexdigest()
        match md5:
            case ROMType.Original.value:
                return TailsAdvPatcher.rom_to_ap(rom)
            case ROMType.VC3DS.value:
                return TailsAdvPatcher.vc3ds_to_original(rom)
            case ROMType.Origins.value:
                return TailsAdvPatcher.origins_to_original(rom)
            case _:
                raise InvalidDataError(f"Supplied base ROM does not match any known MD5 for Tails Adventure (hash of supplied ROM: {md5})")
    
    @staticmethod
    def rom_to_ap(rom: bytes) -> bytes:
        rom = bytearray(rom)
        Patches.apply(rom)
        return bytes(rom)
    
    @staticmethod
    def vc3ds_to_original(rom: bytes) -> bytes:
        patched_rom = bsdiff4.patch(rom, pkgutil.get_data(__name__, "DownPatchVC3DS.bsdiff4"))
        return TailsAdvPatcher.rom_to_ap(patched_rom)
    
    @staticmethod
    def origins_to_original(rom: bytes) -> bytes:
        patched_rom = bsdiff4.patch(rom, pkgutil.get_data(__name__, "DownPatchOrigins.bsdiff4"))
        return TailsAdvPatcher.rom_to_ap(patched_rom)

class TailsAdvPatch(APProcedurePatch):
    game = "Tails Adventure"
    patch_file_ending = ".aptailsadv"
    result_file_ending = ".gg"
    hash = "Multiple"
    procedure = [("apply_tailsadv_patch", [])]

    @classmethod
    def get_source_data(cls) -> bytes:
        from .World import TailsAdvWorld
        return cls.load_base_rom([ROMType.Original.value, ROMType.VC3DS.value, ROMType.Origins.value], TailsAdvWorld.settings.rom_file)

    @classmethod
    def load_base_rom(cls, md5s: List[str], file_name: str) -> bytes:
        if not file_name or not os.path.exists(file_name):
            file_name = Utils.user_path(file_name)

        with open(file_name, "rb") as file:
            rom = file.read()

        md5 = hashlib.md5(rom).hexdigest()
        if md5 in md5s:
            return rom
        else:
            raise InvalidDataError(f"Supplied base ROM does not match any known MD5 for Tails Adventure (hash of supplied ROM: {md5})")