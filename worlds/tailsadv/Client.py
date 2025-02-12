import base64
import logging
import time

from enum import Enum

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from .ROM import ROMType

import worlds._bizhawk as bizhawk

logger = logging.getLogger("Client")

DataKeys = Enum("DataKeys", [
    ("ItemsPage1", "ItemsPage1"),
    ("ItemsPage2", "ItemsPage2"),
    ("ItemsPage3", "ItemsPage3"),
    ("ItemsPageSub", "ItemsPageSub"),
    ("CurrentHealth", "CurrentHealth"),
    ("LevelID", "LevelID"),
    ("RoomID", "RoomID")
])

data_locations = {
    DataKeys.ItemsPage1: (0x1030, 0x01),
    DataKeys.ItemsPage2: (0x1031, 0x01),
    DataKeys.ItemsPage3: (0x1032, 0x01),
    DataKeys.ItemsPageSub: (0x1033, 0x01),
    DataKeys.CurrentHealth: (0x1039, 0x01),
    DataKeys.LevelID: (0x12aa, 0x01),
    DataKeys.RoomID: (0x12ab, 0x01)
}

class TailsAdvClient(BizHawkClient):
    system = "GG"
    patch_suffix = ".aptailsadv"
    game = "Tails Adventure"

    async def validate_rom(self, ctx) -> bool:
        if ctx.rom_hash.lower() in [
            ROMType.Original.value,
            ROMType.VC3DS.value,
            ROMType.Origins.value
        ]:
            ctx.game = self.game
            ctx.items_handling = 0b111
            ctx.finished_game = False
            ctx.current_items_page_1 = None
            ctx.current_items_page_2 = None
            ctx.current_items_page_3 = None
            ctx.current_items_page_sub = None
            ctx.current_level_id = None
            ctx.current_room_id = None
            return True
        return False
    
    def on_package(self, ctx, cmd: str, args: dict) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def game_watcher(self, ctx) -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return
        
        # Read important RAM values
        data = await bizhawk.read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], "RAM")
                                                    for loc_data in data_locations.values()])
        data = {data_set_name: data_name for data_set_name, data_name in zip(data_locations.keys(), data)}

        # Save key data on the server
        items_page_1 = data[DataKeys.ItemsPage1][0]
        items_page_2 = data[DataKeys.ItemsPage2][0]
        items_page_3 = data[DataKeys.ItemsPage3][0]
        items_page_sub = data[DataKeys.ItemsPageSub][0]
        level_id = data[DataKeys.LevelID][0]
        room_id = data[DataKeys.RoomID][0]

        messages = []
        if ctx.current_items_page_1 != items_page_1: messages.append(create_set_data_message("items_page_1", ctx.slot, ctx.team, items_page_1))
        if ctx.current_items_page_2 != items_page_1: messages.append(create_set_data_message("items_page_2", ctx.slot, ctx.team, items_page_2))
        if ctx.current_items_page_3 != items_page_1: messages.append(create_set_data_message("items_page_3", ctx.slot, ctx.team, items_page_3))
        if ctx.current_items_page_sub != items_page_1: messages.append(create_set_data_message("items_page_sub", ctx.slot, ctx.team, items_page_sub))
        if ctx.level_id != level_id: messages.append(create_set_data_message("level_id", ctx.slot, ctx.team, level_id))
        if ctx.room_id != room_id: messages.append(create_set_data_message("room_id", ctx.slot, ctx.team, room_id))
        if messages.count() > 0:
            await ctx.send_msgs(messages)
        
        # Check for goal condition - current health is set to 0xff when the game is beaten
        if data[DataKeys.CurrentHealth][0] == 0xff and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
    
def create_set_data_message(key: str, slot: int, team: int, value: int):
    return {
        "cmd": "Set",
        "key": f"tailsadv_{slot}_{team}_{key}",
        "default": 0,
        "want_reply": True,
        "operations": [{ "operation": "replace", "value": value }]
    }