from enum import Enum
from typing import TYPE_CHECKING

from NetUtils import ClientStatus
from worlds._bizhawk import ConnectionStatus, RequestFailedError
from worlds._bizhawk.client import BizHawkClient
from .Items import item_data_table, item_groups

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

import logging
import worlds._bizhawk as bizhawk

def stored_data_key(team: int|None, slot: int|None, key: str) -> str:
    return f"tailsadv_{team}_{slot}_{key}"

logger = logging.getLogger("Client")

PatchedRomSHA1: str = "62998f9e56655ed18c127f0194e41371de86cc82"

RAM_LABEL: str = "Main RAM"
SENTINEL_VALUE: int = 0xff
WORLD_MAP_ID: int = 16

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
    ("MaximumHealth", "maximum_health"),
    ("CurrentHealth", "current_health"),
    ("EmeraldCount", "emerald_count"),
    ("FlightTime", "flight_time"),
    ("LevelID", "level_id"),
    ("RoomID", "room_id")
])

persisted_state_data_locations: dict[DataKeys, tuple[int, int]] = {
    DataKeys.ItemsPage1: (0x1030, 0x01),
    DataKeys.ItemsPage2: (0x1031, 0x01),
    DataKeys.ItemsPage3: (0x1032, 0x01),
    DataKeys.ItemsPageSub: (0x1033, 0x01),
    DataKeys.MaximumHealth: (0x1038, 0x01),
    DataKeys.EmeraldCount: (0x103a, 0x01),
    DataKeys.FlightTime: (0x103c, 0x01),
}

session_state_data_locations: dict[DataKeys, tuple[int, int]] = {
    DataKeys.SelectedItem1: (0x1020, 0x01),
    DataKeys.SelectedItem2: (0x1021, 0x01),
    DataKeys.SelectedItem3: (0x1022, 0x01),
    DataKeys.SelectedItem4: (0x1023, 0x01),
    DataKeys.ItemObtained: (0x1037, 0x01),
    DataKeys.MaximumHealth: (0x1038, 0x01),
    DataKeys.CurrentHealth: (0x1039, 0x01),
    DataKeys.EmeraldCount: (0x103a, 0x01),
    DataKeys.FlightTime: (0x103c, 0x01),
    DataKeys.LevelID: (0x12aa, 0x01),
    DataKeys.RoomID: (0x12ab, 0x01),
    DataKeys.ItemPickup: (0x12f5, 0x01)
}

item_page_bit_map: dict[int, tuple[int, int]] = {
    data.code: (data.page, data.bit) for data in item_data_table.values()
}

health_flight_map: dict[int, tuple[int, int]] = {
    0: (10, 2),
    1: (20, 4),
    2: (30, 6),
    3: (40, 8),
    4: (50, 10),
    5: (60, 11),
    6: (99, 12),
}

class TailsAdvClient(BizHawkClient):
    system = "GG"
    patch_suffix = ".aptailsadv"
    game = "Tails Adventure"
    current_level_id: int|None
    current_area_id: int|None
    current_index: int

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        if (ctx.rom_hash or "").lower() == PatchedRomSHA1:
            ctx.game = self.game
            ctx.items_handling = 0b111
            ctx.finished_game = False
            self.current_level_id = None
            self.current_area_id = None
            self.current_index = 0
            return True
        return False
    
    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        match cmd:
            case "RoomInfo":
                ctx.seed_name = args["seed_name"]
            case "Connected":
                ctx.set_notify(
                    stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage1.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage2.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage3.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPageSub.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.MaximumHealth.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.EmeraldCount.value),
                    stored_data_key(ctx.team, ctx.slot, DataKeys.FlightTime.value)
                )

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        connected_to_ap = ctx.server and ctx.server.socket.open
        connected_to_bizhawk = ctx.bizhawk_ctx.connection_status == ConnectionStatus.CONNECTED
        if not connected_to_ap or not connected_to_bizhawk:
            return
        
        try:
            # Read session state values
            session_state_data = await bizhawk.read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], RAM_LABEL)
                                                                      for loc_data
                                                                      in session_state_data_locations.values()])
            session_state_data = dict(zip(session_state_data_locations.keys(), (d[0] for d in session_state_data)))
            item_obtained = session_state_data[DataKeys.ItemObtained]
            item_pickup = session_state_data[DataKeys.ItemPickup]
            level_id = session_state_data[DataKeys.LevelID]
            room_id = session_state_data[DataKeys.RoomID]
            current_health = session_state_data[DataKeys.CurrentHealth]

            await self.__set_correct_inventory(ctx, level_id)
            await self.__process_location_check(ctx, item_obtained, item_pickup)
            await self.__process_received_items(ctx, session_state_data)
            await self.__send_map_update(ctx, level_id, room_id)
            await self.__check_goal_condition(ctx, current_health)
        except RequestFailedError as rfe:
            logger.warning(f"Unable to synchronise game state: {rfe.args[0]}")
            logger.warning("Please wait until the connection to BizHawk is restored")
            return

    async def __set_correct_inventory(self, ctx: "BizHawkClientContext", level_id: int):
        if self.current_level_id != level_id and level_id == WORLD_MAP_ID:
            items_page_1 = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage1.value)) or 0
            items_page_2 = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage2.value)) or 0
            items_page_3 = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPage3.value)) or 0
            items_page_sub = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.ItemsPageSub.value)) or 0
            maximum_health = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.MaximumHealth.value)) or 0
            emerald_count = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.EmeraldCount.value)) or 0
            flight_time = ctx.stored_data.get(stored_data_key(ctx.team, ctx.slot, DataKeys.FlightTime.value)) or 0
            data = [items_page_1, items_page_2, items_page_3, items_page_sub, maximum_health, emerald_count, flight_time]
            await bizhawk.write(ctx.bizhawk_ctx, [(loc_data[0], [value], RAM_LABEL)
                                                  for value, loc_data
                                                  in zip(data, persisted_state_data_locations.values())])

    async def __process_location_check(self, ctx: "BizHawkClientContext", item_obtained: int, item_pickup: int):
        if item_pickup == SENTINEL_VALUE and item_obtained:
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                # The Chaos Emeralds have IDs from 27 to 32 in AP and 32 to 37 in the game, hence the conversion
                "locations": [item_obtained - 5 if 32 <= item_obtained <= 37 else item_obtained]
            }])

    async def __process_received_items(self, ctx: "BizHawkClientContext", session_state_data: dict[DataKeys, int]):
        while self.current_index < len(ctx.items_received):
            item_id = ctx.items_received[self.current_index].item
            item_name = ctx.item_names.lookup_in_game(item_id)
            self.current_index += 1
            await self.__update_persisted_inventory(ctx, item_id)
            if item_name in item_groups["Field Equipment"] or item_name in item_groups["Submarine Equipment"]:
                await self.__update_selected_inventory(ctx, session_state_data, item_id)
            elif item_name in item_groups["Chaos Emeralds"]:
                await self.__update_health_and_flight(ctx, session_state_data)
            elif item_name == "Ring":
                await self.__heal(ctx, session_state_data)

    async def __update_persisted_inventory(self, ctx: "BizHawkClientContext", item_id: int):
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
                return
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": stored_data_key(ctx.team, ctx.slot, page),
            "default": 0,
            "want_reply": True,
            "operations": [{ "operation": "or", "value": (1 << bit) }]
        }])

    async def __update_selected_inventory(self, ctx: "BizHawkClientContext", session_state_data: dict[DataKeys, int], item_id: int):
        selected_item_1 = session_state_data[DataKeys.SelectedItem1]
        selected_item_2 = session_state_data[DataKeys.SelectedItem2]
        selected_item_3 = session_state_data[DataKeys.SelectedItem3]
        selected_item_4 = session_state_data[DataKeys.SelectedItem4]
        if not selected_item_1:
            selected_item_1 = item_id
            await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.SelectedItem1][0], [selected_item_1], RAM_LABEL)])
        elif not selected_item_2:
            selected_item_2 = item_id
            await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.SelectedItem2][0], [selected_item_2], RAM_LABEL)])
        elif not selected_item_3:
            selected_item_3 = item_id
            await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.SelectedItem3][0], [selected_item_3], RAM_LABEL)])
        elif not selected_item_4:
            selected_item_4 = item_id
            await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.SelectedItem4][0], [selected_item_4], RAM_LABEL)])

    async def __update_health_and_flight(self, ctx: "BizHawkClientContext", session_state_data: dict[DataKeys, int]):
        emerald_count = session_state_data[DataKeys.EmeraldCount]
        if emerald_count < 6:
            emerald_count += 1
            (new_health, new_flight) = health_flight_map[emerald_count]
            keys = [DataKeys.MaximumHealth, DataKeys.CurrentHealth, DataKeys.EmeraldCount, DataKeys.FlightTime]
            data = [new_health, new_health, emerald_count, new_flight]
            await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[loc_data][0], [value], RAM_LABEL)
                                                  for value, loc_data
                                                  in zip(data, keys)])
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": stored_data_key(ctx.team, ctx.slot, DataKeys.MaximumHealth.value),
                "default": 0,
                "want_reply": False,
                "operations": [{ "operation": "replace", "value": new_health }]
            },
            {
                "cmd": "Set",
                "key": stored_data_key(ctx.team, ctx.slot, DataKeys.EmeraldCount.value),
                "default": 0,
                "want_reply": False,
                "operations": [{ "operation": "replace", "value": emerald_count }]
            },
            {
                "cmd": "Set",
                "key": stored_data_key(ctx.team, ctx.slot, DataKeys.FlightTime.value),
                "default": 0,
                "want_reply": False,
                "operations": [{ "operation": "replace", "value": new_flight }]
            }])

    async def __heal(self, ctx: "BizHawkClientContext", session_state_data: dict[DataKeys, int]):
        maximum_health = session_state_data[DataKeys.MaximumHealth]
        current_health = session_state_data[DataKeys.CurrentHealth]
        if current_health < maximum_health:
            current_health += 1
            await bizhawk.write(ctx.bizhawk_ctx, [(session_state_data_locations[DataKeys.CurrentHealth][0], [current_health], RAM_LABEL)])

    async def __send_map_update(self, ctx: "BizHawkClientContext", level_id: int, area_id: int):
        if self.current_level_id != level_id or self.current_area_id != area_id:
            self.current_level_id = level_id
            self.current_area_id = area_id
            await ctx.send_msgs([{
                "cmd": "Bounce",
                "slots": [ctx.slot],
                "data": { "level": level_id, "area": area_id }
            }])

    async def __check_goal_condition(self, ctx: "BizHawkClientContext", current_health: int):
        if current_health == SENTINEL_VALUE and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True