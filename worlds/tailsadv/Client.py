import base64
import logging
import time

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from .ROM import ROMType

import worlds._bizhawk as bizhawk

logger = logging.getLogger("Client")

class TailsAdvClient(BizHawkClient):
    system = "GG"
    patch_suffix = ".aptailsadv"
    game = "Tails Adventure"

    async def validate_rom(self, ctx) -> bool:
        print(ctx.rom_hash)
        if ctx.rom_hash in [
            ROMType.Original.value,
            ROMType.VC3DS.value,
            ROMType.Origins.value
        ]:
            ctx.game = self.game
            ctx.items_handling = 0b111
            ctx.finished_game = False
            return True
        return False
    
    def on_package(self, ctx, cmd: str, args: dict) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def set_auth(self, ctx) -> None:
        ctx.auth = self.player_name

    async def game_watcher(self, ctx) -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return