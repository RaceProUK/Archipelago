def apply(rom: bytearray) -> None:
    __disable_lives_system(rom)
    __always_show_pickups(rom)
    __disable_inventory_updates(rom)
    __force_new_game(rom)
    __preserve_player_state_on_new_game(rom)
    __disable_password_access(rom)

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

# Sets the default option to NEW GAME and prevents selection of CONTINUE
def __force_new_game(rom: bytearray) -> None:
    # Sets the default option to NEW GAME
    rom[0x00833] = 0x00 # ld a, $01 => ld a, $00

    # Prevents selection of CONTINUE
    rom[0x0090e] = 0x00 # inc a     => nop

    # Fixes the selector position
    rom[0x0092a] = 0x0e # ld a, $00 => ld a, $0e
    rom[0x0092f] = 0x00 # ld a, $0e => ld a, $00

# Don't wipe inventory and progression when starting the game
def __preserve_player_state_on_new_game(rom: bytearray) -> None:
    rom[0x00854] = 0x40 # ld hl, $1010 => ld hl, $1040
    rom[0x00857] = 0x40 # ld de, $1011 => ld de, $1041
    rom[0x0085a] = 0xa4 # ld bc, $00d4 => ld bc, $00a4

# When the player attempts to access the password screen
# Instead kick them out to the World Map :D
def __disable_password_access(rom: bytearray) -> None:
    rom[0x2c060] = 0x00 # jp z, $82d3 => nop
    rom[0x2c061] = 0x00 #                nop
    rom[0x2c062] = 0x00 #                nop