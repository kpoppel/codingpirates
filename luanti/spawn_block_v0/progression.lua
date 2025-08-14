-- This file contains lists of blocks and entities that can be spawned in the world.
-- The blocks are used to replace the block under the player when dug.
-- As the game progresses more blocks are made available to the player.

progression = {}

progression.block_list = {
    -- block level 1
    "default:dirt",
    "default:tree",
    "default:dirt_with_grass",

    -- block level 2 - after wood pickaxe
    "default:stone",
    --"default:leaves",

    -- block level 3 - after stone pickaxe
    -- "bronze",
    -- "tin",
    -- "papyrus",
    -- "sand",
    -- "gravel",
    -- "jungle tree"

    -- block level 4 - after bronze pickaxe
    -- "iron",
    -- "coal",
    -- "cactus",
    -- "clay" -- uselsss
    -- block level 5 - after steel pickaxe
    -- "mese",
    -- "bones"
    -- "gold",
    -- block level 6 - after mese pickaxe

    -- "diamond"
    -- block level 7 - after diamond pickaxe
}

progression.entity_list = {
    -- tree sapling
    "bucket:bucket_empty",
    --"tnt:tnt"
    -- flowers, 
    --"snow"
    -- cotton
    -- bush stems (useless)
    -- butterfly
    -- firefly
    -- seeds
}

return progression
-- End of spawn_block/progression.lua