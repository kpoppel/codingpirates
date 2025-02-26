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
    "default:leaves",

    -- block level 3 - after stone pickaxe
    "default:stone_with_coal",
    "default:stone_with_copper",
    "default:stone_with_tin",
    "default:sand",
    "default:gravel",
    "default:jungletree",

    -- block level 4 - after bronze pickaxe
    "default:stone_with_iron",
    "default:cactus",
    "default:clay",
    
    -- block level 5 - after steel pickaxe
    "default:stone_with_mese",
    "default:stone_with_gold",

    -- block level 6 - after mese pickaxe
    "default:stone_with_diamond"
    
    -- block level 7 - after diamond pickaxe
}

progression.entity_list = {
    -- tree sapling
    "bucket:bucket_water",
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