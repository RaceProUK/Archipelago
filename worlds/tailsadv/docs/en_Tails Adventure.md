# Tails Adventure

## What is this game?

Tails Adventure (テイルスアドベンチャー) is a mini-Metroidvania starring Miles 'Tails' Prower, released in 1995 for the Sega Game Gear.

## What is the goal of Tails Adventure?

To drive the invading Battle Kukku Empire from Cocoa Island by infiltrating their Battle Fortress and defeating Dr Fukurokov, Battle Kukku 16th (a.k.a. Speedy), and ultimately Great Battle Kukku 15th, the leader of the Battle Kukku Army.

## Where is the options page?

[Player Options](../player-options) contains everything required to configure and export a YAML configuration file for this game.

## What does randomization do to this game?

The locations of the thirty items collected across Cocoa Island are randomized.

Two items are not randomized as they are always given to the player when starting a new game: the Regular Bomb and the Vulcan Gun.

## What are location checks?

Any of the thirty locations where an item is normally picked up. Most of these are simply capsules placed around the various levels, but a handful are dropped by bosses on defeat.

## Which items can be in another player's world?

All items can potentially appear in other players' worlds, with the exception of the Regular Bomb and the Vulcan Gun, both of which the player always starts with.

## When a player receives an item, what happens?

When an inventory item is received while online, the item will be added to the player's inventory and the vanilla sound cue will play. There won't be an in-game notification to avoid interrupting gameplay at an inopportune moment.

When a Ring is received, the vanilla behaviour is preserved i.e. the health will increment by 1 (unless already at the maximum) and the sound cue will play.

Inventory items received offline will be added to the player's inventory the next time they connect to the multiworld.

In all cases, the BizHawk Client will show a message for each received item.

## What other changes does the randomiser make?

To help make playing the game a little smoother, a few changes have been made:

- It is no longer possible to Game Over; death simply returns the player to their original spawn within the current map
- Progression and inventory are saved to the Archipelago server; as the password screen no longer serves any purpose, it is no longer accessible
    - The `CONT.` option in Tails' House is now a duplicate of `EXIT` i.e. it returns to the World Map

## Planned changes

- Go straight from `PRESS START` on the title screen to the World Map
- Remove `CONT.` from Tails' House entirely
- Replace in-game pickup icons with a custom AP icon and the text captions with `AP ITEM`
    - Icons and captions in Tails' House will remain as vanilla, including both `RAIDO` and `ROCKET BOOTER`