import logging
import os
import hashlib
import bsdiff4
import pkgutil
import Utils

from enum import Enum
from typing import List

from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APPatchExtension, InvalidDataError

logger = logging.getLogger("ROM")

ROMType = Enum("ROMType", [
    ("Original", "a8bdb1beed088ff83c725c5af6b85e1f"), # Also SADX and Gems
    ("VC3DS", "c2fe111a6e569ec6d58b9ecc32de0e12"),
    ("Origins", "9a2892a5c14b52d517ec74685365314f")
])

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
        # Disable Game Over screen by deducting zero from the life count on death
        # Specifically, 0x1217 is the operand to the opcode at 0x1216
        # The full Z80 instruction is `sub $01`, which we patch to `sub $00`
        # Did you know Tails Adventure has a life system? You do now!
        rom[0x01217] = 0x00

        # Disable the game's default item pickup handling placing the item in the inventory
        # Instead, inventory will be managed by Archipelago via data storage and the BizHawk connector
        rom[0x352ad] = 0x00
        rom[0x352ae] = 0x00
        rom[0x352af] = 0x00
        rom[0x352c3] = 0x00
        rom[0x352c4] = 0x00
        rom[0x352c5] = 0x00
        rom[0x352c6] = 0x00
        rom[0x352c7] = 0x00
        rom[0x352c8] = 0x00
        rom[0x352c9] = 0x00
        rom[0x352ca] = 0x00
        rom[0x352cb] = 0x00
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
        return load_base_rom([ROMType.Original.value, ROMType.VC3DS.value, ROMType.Origins.value])

def load_base_rom(md5s: List[str], file_name: str = "") -> bytes:
    options = Utils.get_options()
    if not file_name:
        file_name = options["tailsadv_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    with open(file_name, "rb") as file:
        rom = file.read()
    md5 = hashlib.md5(rom).hexdigest()
    if md5 in md5s:
        return rom
    else:
        raise InvalidDataError(f"Supplied base ROM does not match any known MD5 for Tails Adventure (hash of supplied ROM: {md5})")