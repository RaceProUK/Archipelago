def apply(rom: bytearray) -> None:
    __disable_lives_system(rom)
    __always_show_pickups(rom)
    __disable_inventory_updates(rom)

# Disable Game Over screen by deducting zero from the life count on death
# If we don't decrement lives, we never get a Game Over
# Did you know Tails Adventure has a lives system? You do now!
def __disable_lives_system(rom: bytearray) -> None:
    rom[0x01217] = 0x00 # sub $01 => sub $00

# Disable writing the sentinel value that hides collected items
# This ensures that we can still do a location check even if we have the vanilla item
def __always_show_pickups(rom: bytearray) -> None:
    rom[0x352a3] = 0x00 # ld (ix+0), $FF => nop
    rom[0x352a4] = 0x00 #                => nop
    rom[0x352a5] = 0x00 #                => nop
    rom[0x352a6] = 0x00 #                => nop

# Disable the game's default item pickup handling placing the item in the inventory
# Instead, inventory will be managed by Archipelago via data storage and the BizHawk connector
def __disable_inventory_updates(rom: bytearray) -> None:
    rom[0x352ad] = 0x00 # call $93c5 => nop (disables adding to current inventory and updating max health and flight meter)
    rom[0x352ae] = 0x00 #               nop
    rom[0x352af] = 0x00 #               nop
    rom[0x352c3] = 0x00 # inc hl     => nop (disables adding to inventory in Tails' House)
    rom[0x352c4] = 0x00 # ld e, (hl) => nop
    rom[0x352c5] = 0x00 # inc hl     => nop
    rom[0x352c6] = 0x00 # ld d, (hl) => nop
    rom[0x352c7] = 0x00 # inc hl     => nop
    rom[0x352c8] = 0x00 # ld b, (hl) => nop
    rom[0x352c9] = 0x00 # ld a, (de) => nop
    rom[0x352ca] = 0x00 # or b       => nop
    rom[0x352cb] = 0x00 # ld (de), a => nop