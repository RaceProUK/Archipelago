import logging

from enum import Enum

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from .Items import item_data_table, item_groups

import worlds._bizhawk as bizhawk

def stored_data_key(team: int, slot: int, key: str) -> str:
    return f"tailsadv_{team}_{slot}_{key}"

logger = logging.getLogger("Client")

PatchedRomSHA1 = "62998f9e56655ed18c127f0194e41371de86cc82"

RAM_LABEL = "Main RAM"
SENTINEL_VALUE = 0xff
WORLD_MAP_ID = 16

DataKeys = Enum("DataKeys", [
    ("SelectedItem1", "selected_item_1"),
    ("SelectedItem2", "selected_item_2"),
    ("SelectedItem3", "selected_item_3"),
    ("SelectedItem4", "selected_item_4"),
    ("ItemsPage1", "items_page_1"),
    ("ItemsPage2", "items_page_2"),
    ("ItemsPage3", "items_page_3"),
    ("ItemsPageSub", "items_page_sub"),
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
    DataKeys.SelectedItem1: (0x1020, 0x01),
    DataKeys.SelectedItem2: (0x1021, 0x01),
    DataKeys.SelectedItem3: (0x1022, 0x01),
    DataKeys.SelectedItem4: (0x1023, 0x01),
    DataKeys.ItemObtained: (0x1037, 0x01),
    DataKeys.CurrentHealth: (0x1039, 0x01),
    DataKeys.LevelID: (0x12aa, 0x01),
    DataKeys.RoomID: (0x12ab, 0x01),
    DataKeys.ItemPickup: (0x12f5, 0x01)
}

item_page_bit_map = {
    data.code: (data.page, data.bit) for data in item_data_table.values()
}

class TailsAdvClient(BizHawkClient):
    system = "GG"
    patch_suffix = ".aptailsadv"
    game = "Tails Adventure"

    async def validate_rom(self, ctx) -> bool:
        if ctx.rom_hash.lower() == PatchedRomSHA1:
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
                ctx.set_notify(
                    stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage1.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage2.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage3.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPageSub.value)
                )

    async def game_watcher(self, ctx) -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return
        
        # Read session state values
        session_state_data = await bizhawk.read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], RAM_LABEL)
                                                                  for loc_data
                                                                  in session_state_data_locations.values()])
        session_state_data = {data_set_name: data_name
                              for data_set_name, data_name
                              in zip(session_state_data_locations.keys(), session_state_data)}
        item_obtained = session_state_data[DataKeys.ItemObtained][0]
        item_pickup = session_state_data[DataKeys.ItemPickup][0]
        level_id = session_state_data[DataKeys.LevelID][0]
        room_id = session_state_data[DataKeys.RoomID][0]
        current_health = session_state_data[DataKeys.CurrentHealth][0]

        await self.__set_correct_inventory(ctx, level_id)
        await self.__process_location_check(ctx, item_obtained, item_pickup)
        await self.__process_received_items(ctx, session_state_data)
        await self.__save_session_state_to_server(ctx, level_id, room_id)
        await self.__check_goal_condition(ctx, current_health)

    async def __set_correct_inventory(self, ctx, level_id):
        if ctx.current_level_id != level_id and level_id == WORLD_MAP_ID:
            items_page_1 = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage1.value)) or 0
            items_page_2 = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage2.value)) or 0
            items_page_3 = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage3.value)) or 0
            items_page_sub = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPageSub.value)) or 0
            data = [items_page_1, items_page_2, items_page_3, items_page_sub]
            await bizhawk.write(ctx.bizhawk_ctx, [(loc_data[0], [value], RAM_LABEL)
                                                  for value, loc_data
                                                  in zip(data, persisted_state_data_locations.values())])

    async def __process_location_check(self, ctx, item_obtained, item_pickup):
        if item_pickup == SENTINEL_VALUE and item_obtained:
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                # The Chaos Emeralds have IDs from 27 to 32 in AP and 32 to 37 in the game, hence the conversion
                "locations": [item_obtained - 5 if 32 <= item_obtained <= 37 else item_obtained]
            }])

    async def __process_received_items(self, ctx, session_state_data):
        selected_item_1 = session_state_data[DataKeys.SelectedItem1][0]
        selected_item_2 = session_state_data[DataKeys.SelectedItem2][0]
        selected_item_3 = session_state_data[DataKeys.SelectedItem3][0]
        selected_item_4 = session_state_data[DataKeys.SelectedItem4][0]
        while ctx.current_index < len(ctx.items_received):
            item_id = ctx.items_received[ctx.current_index].item
            item_name = ctx.item_names.lookup_in_game(item_id)
            ctx.current_index += 1

            # Update persisted inventory
            page, bit = item_page_bit_map[item_id]
            match page:
                case 1:
                    page = DataKeys.ItemsPage1.value
                case 2:
                    page = DataKeys.ItemsPage2.value
                case 3:
                    page = DataKeys.ItemsPage3.value
                case 4:                    
                    page = DataKeys.ItemsPageSub.value
                case _:
                    continue
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": stored_data_key(ctx.team, ctx.slot, page),
                "default": 0,
                "want_reply": True,
                "operations": [{ "operation": "or", "value": (1 << bit) }]
            }])

            if item_name in item_groups["Field Equipment"] or item_name in item_groups["Submarine Equipment"]:
                # If field/Sea Fox item, add to current inventory
                if not selected_item_1:
                    selected_item_1 = item_id
                    await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.SelectedItem1][0], selected_item_1, RAM_LABEL)])
                elif not selected_item_2:
                    selected_item_2 = item_id
                    await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.SelectedItem2][0], selected_item_2, RAM_LABEL)])
                elif not selected_item_3:
                    selected_item_3 = item_id
                    await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.SelectedItem3][0], selected_item_3, RAM_LABEL)])
                elif not selected_item_4:
                    selected_item_4 = item_id
                    await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.SelectedItem4][0], selected_item_4, RAM_LABEL)])
            elif item_name in item_groups["Chaos Emeralds"]:
                # If Chaos Emerald, heal and increase max health and flight meter
                pass
            else:
                match item_name:
                    case "Ring":
                        pass

    async def __save_session_state_to_server(self, ctx, level_id, room_id):
        def set_data_message(key: str, value: int) -> dict:
            return {
                "cmd": "Set",
                "key": stored_data_key(ctx.team, ctx.slot, key),
                "default": 0,
                "want_reply": False,
                "operations": [{ "operation": "replace", "value": value }]
            }
        messages = []
        if ctx.current_level_id != level_id:
            messages.append(set_data_message(DataKeys.LevelID.value, level_id))
            ctx.current_level_id = level_id
        if ctx.current_room_id != room_id:
            messages.append(set_data_message(DataKeys.RoomID.value, room_id))
            ctx.current_room_id = room_id
        if len(messages) > 0:
            await ctx.send_msgs(messages)

    async def __check_goal_condition(self, ctx, current_health):
        if current_health == SENTINEL_VALUE and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True