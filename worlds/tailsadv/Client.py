import logging

from enum import Enum

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from .ROM import ROMType

import worlds._bizhawk as bizhawk

logger = logging.getLogger("Client")

SENTINEL_VALUE = 0xff
WORLD_MAP_ID = 16

DataKeys = Enum("DataKeys", [
    ("ItemsPage1", "items_page_1"),
    ("ItemsPage2", "items_page_2"),
    ("ItemsPage3", "items_page_3"),
    ("ItemsPageSub", "items_page+sub"),
    ("ItemObtained", "item_obtained"),
    ("ItemPickup", "item_pickup"),
    ("CurrentHealth", "current_health"),
    ("LevelID", "level_id"),
    ("RoomID", "room_id")
])

persisted_state_data_locations = {
    DataKeys.ItemsPage1: (0x1030, 0x01),
    DataKeys.ItemsPage2: (0x1031, 0x01),
    DataKeys.ItemsPage3: (0x1032, 0x01),
    DataKeys.ItemsPageSub: (0x1033, 0x01),
}

session_state_data_locations = {
    DataKeys.ItemObtained: (0x1037, 0x01),
    DataKeys.CurrentHealth: (0x1039, 0x01),
    DataKeys.LevelID: (0x12aa, 0x01),
    DataKeys.RoomID: (0x12ab, 0x01),
    DataKeys.ItemPickup: (0x12ab, 0x01)
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
            ctx.current_level_id = None
            ctx.current_room_id = None
            ctx.current_index = 0
            return True
        return False
    
    def on_package(self, ctx, cmd: str, args: dict) -> None:
        match cmd:
            case "RoomInfo":
                ctx.seed_name = args["seed_name"]
            case "Connected":
                ctx.set_notify([
                    f"tailsadv_{ctx.slot}_{ctx.team}_{DataKeys.ItemsPage1.value()}",
                    f"tailsadv_{ctx.slot}_{ctx.team}_{DataKeys.ItemsPage2.value()}",
                    f"tailsadv_{ctx.slot}_{ctx.team}_{DataKeys.ItemsPage3.value()}",
                    f"tailsadv_{ctx.slot}_{ctx.team}_{DataKeys.ItemsPageSub.value()}"
                ])

    async def game_watcher(self, ctx) -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return
        
        # Read important RAM values
        persisted_data = await bizhawk.read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], "RAM")
                                                              for loc_data in persisted_state_data_locations.values()])
        session_state_data = await bizhawk.read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], "RAM")
                                                                  for loc_data in session_state_data_locations.values()])
        persisted_data = {data_set_name: data_name
                          for data_set_name, data_name
                          in zip(persisted_state_data_locations.keys(), persisted_data)}
        session_state_data = {data_set_name: data_name
                              for data_set_name, data_name
                              in zip(session_state_data_locations.keys(), session_state_data)}
        items_page_1 = persisted_data[DataKeys.ItemsPage1][0]
        items_page_2 = persisted_data[DataKeys.ItemsPage2][0]
        items_page_3 = persisted_data[DataKeys.ItemsPage3][0]
        items_page_sub = persisted_data[DataKeys.ItemsPageSub][0]
        item_obtained = session_state_data[DataKeys.ItemObtained][0]
        item_pickup = session_state_data[DataKeys.ItemPickup][0]
        level_id = session_state_data[DataKeys.LevelID][0]
        room_id = session_state_data[DataKeys.RoomID][0]
        current_health = session_state_data[DataKeys.CurrentHealth][0]

        # Ensure game inventory is correct when on map screen        
        if ctx.room_id != room_id and room_id == WORLD_MAP_ID:
            items_page_1 = int(ctx.stored_data.get(f"tailsadv_{ctx.slot}_{ctx.team}_{DataKeys.ItemsPage1.value()}", 0))
            items_page_2 = int(ctx.stored_data.get(f"tailsadv_{ctx.slot}_{ctx.team}_{DataKeys.ItemsPage2.value()}", 0))
            items_page_3 = int(ctx.stored_data.get(f"tailsadv_{ctx.slot}_{ctx.team}_{DataKeys.ItemsPage3.value()}", 0))
            items_page_sub = int(ctx.stored_data.get(f"tailsadv_{ctx.slot}_{ctx.team}_{DataKeys.ItemsPageSub.value()}", 0))
            keys = [(loc_data[0], loc_data[1], "RAM")
                    for loc_data in persisted_state_data_locations.values()]
            data = [items_page_1, items_page_2, items_page_3, items_page_sub]
            await bizhawk.write(zip(keys, data))

        # Process location check
        if item_pickup == SENTINEL_VALUE and item_obtained:
            # TODO: Implement location check
            pass

        # Process received items
        while ctx.current_index < len(ctx.items_received):
            # TODO: Implement receiving item
            ctx.current_index += 1

        # Save live state data on the server        
        def set_data_message(key: str, value: int):
            return {
                "cmd": "Set",
                "key": f"tailsadv_{ctx.slot}_{ctx.team}_{key}",
                "default": 0,
                "want_reply": False,
                "operations": [{ "operation": "replace", "value": value }]
            }
        messages = []
        if ctx.level_id != level_id:
            messages.append(set_data_message(DataKeys.LevelID.value(), level_id))
            ctx.level_id = level_id
        if ctx.room_id != room_id:
            messages.append(set_data_message(DataKeys.RoomID.value(), room_id))
            ctx.room_id = room_id
        if len(messages) > 0:
            await ctx.send_msgs(messages)
        
        # Check for goal condition - current health is set to SENTINEL_VALUE when the game is beaten
        if current_health == SENTINEL_VALUE and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True