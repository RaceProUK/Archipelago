import os
import hashlib
import bsdiff4
import pkgutil
import Utils

from enum import Enum
from typing import List

from worlds.AutoWorld import World
from worlds.Files import APDeltaPatch

ROMType = Enum("ROMType", [
    ("Original", "a8bdb1beed088ff83c725c5af6b85e1f"), # Also SADX and Gems
    ("VC3DS", "c2fe111a6e569ec6d58b9ecc32de0e12"),
    ("Origins", "9a2892a5c14b52d517ec74685365314f")
])

class TailsAdvDeltaPatch(APDeltaPatch):
    patch_file_ending = ".aptailsadv"
    result_file_ending = ".gg"

class OriginalDeltaPatch(TailsAdvDeltaPatch):
    hash = ROMType.Original.value
    @classmethod
    def get_source_data(cls):
        _, rom = load_base_rom([ROMType.Original.value])
        return rom

class VC3DSDeltaPatch(TailsAdvDeltaPatch):
    hash = ROMType.VC3DS.value
    @classmethod
    def get_source_data(cls):
        _, rom = load_base_rom([ROMType.VC3DS.value])
        return rom

class OriginsDeltaPatch(TailsAdvDeltaPatch):
    hash = ROMType.Origins.value
    @classmethod
    def get_source_data(cls):
        _, rom = load_base_rom([ROMType.Origins.value])
        return rom

def generate_output(world: World, output_directory: str) -> None:
    safe_slot_name = world.multiworld.get_file_safe_player_name(world.player).replace(" ", "_")
    rom_name = f"AP_{world.multiworld.seed_name}_P{world.player}_{safe_slot_name}.gg"
    rom_path = os.path.join(output_directory, rom_name)

    romType, data = load_base_rom(world.settings.rom_file.md5s)

    # Down-patch to the original ROM if necessary
    match romType:
        case ROMType.VC3DS:
            patch = pkgutil.get_data(__name__, "DownPatchVC3DS.bsdiff4")
            data = bytes(bsdiff4.patch(data, patch))
        case ROMType.Origins:
            patch = pkgutil.get_data(__name__, "DownPatchOrigins.bsdiff4")
            data = bytes(bsdiff4.patch(data, patch))

    # Write updated ROM
    with open(rom_path, "wb") as outfile:
        outfile.write(data)
    
    # Write patch file
    match romType:
        case ROMType.Original:
            patch = OriginalDeltaPatch(os.path.splitext(rom_path)[0] + TailsAdvDeltaPatch.patch_file_ending,
                                       player = world.player,
                                       player_name = world.multiworld.player_name[world.player],
                                       patched_path = rom_path)
        case ROMType.VC3DS:
            patch = VC3DSDeltaPatch(os.path.splitext(rom_path)[0] + TailsAdvDeltaPatch.patch_file_ending,
                                    player = world.player,
                                    player_name = world.multiworld.player_name[world.player],
                                    patched_path = rom_path)
        case ROMType.Origins:
            patch = OriginsDeltaPatch(os.path.splitext(rom_path)[0] + TailsAdvDeltaPatch.patch_file_ending,
                                      player = world.player,
                                      player_name = world.multiworld.player_name[world.player],
                                      patched_path = rom_path)
    patch.write()
    os.unlink(rom_path)

def load_base_rom(md5s: List[str], file_name: str = "") -> tuple[ROMType, bytes]:
    options = Utils.get_options()
    if not file_name:
        file_name = options["tailsadv_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    with open(file_name, "rb") as file:
        rom = file.read()
    md5 = hashlib.md5()
    md5.update(rom)
    hex = md5.hexdigest()
    if hex in md5s:
        return ROMType(hex), rom
    else:
        raise Exception("Supplied base ROM does not match the known MD5 for Tails Adventure")