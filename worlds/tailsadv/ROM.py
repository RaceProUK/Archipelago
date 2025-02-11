import os
import hashlib
import Utils

from typing import List

from worlds.AutoWorld import World

def generate_output(world: World, output_directory: str) -> None:
    safe_slot_name = world.multiworld.get_file_safe_player_name(world.player).replace(" ", "_")
    rom_name = f"AP_{world.multiworld.seed_name}_P{world.player}_{safe_slot_name}.gg"
    rom_path = os.path.join(output_directory, rom_name)

    data = load_base_rom(world.settings.rom_file.md5s)
    with open(rom_path, "wb") as outfile:
        outfile.write(data)
    os.unlink(rom_path)

def load_base_rom(md5s: List[str], file_name: str = "") -> bytes:
    options = Utils.get_options()
    if not file_name:
        file_name = options["tailsadv_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    with open(file_name, "rb") as file:
        rom = file.read()
    md5 = hashlib.md5()
    md5.update(rom)
    if md5.hexdigest() in md5s:
        return rom
    else:
        raise Exception("Supplied base ROM does not match the known MD5 for Tails Adventure")