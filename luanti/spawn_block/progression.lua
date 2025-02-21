-- This file contains lists of blocks and entities that can be spawned in the world.
-- The blocks are used to replace the block under the player when dug.
-- As the game progresses more blocks are made available to the player.

progression = {}

progression.block_list = {
    -- block level 1
    "default:dirt",
    "default:tree",
    "default:dirt_with_grass",

    -- block level 2
    "default:stone",
    "default:leaves",
}

progression.entity_list = {
    "bucket:bucket_empty",
    --"tnt:tnt"
}

return progression
-- End of spawn_block/progression.lua