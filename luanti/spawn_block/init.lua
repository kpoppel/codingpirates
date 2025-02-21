local modname = core.get_current_modname()
local modpath = core.get_modpath(modname)
dofile(modpath .. DIR_DELIM .. "player_spawn.lua")
local progression = dofile(modpath .. DIR_DELIM .. "progression.lua")

-- One_block game.
--   Initially the player will have access to only a few different blocks, like
--   dirt, and wood.
--   Once the player has constructed a wood pickaxe, they will have access to
--   more blocks, like stone.
--   Similarly as the game progresses certain entities will be made available to
--   the player.  This could be a bucket with water and lave to enable creating a
--   stone factory.

-- When the player digs the first block it returns itself and replaces it with a
-- randomly chosen block from the list of blocks available to the player at that time.
allowed_block_level = 3
allowed_entity_level = 0
core.register_on_dignode(function(pos, oldnode, digger)
    if core.get_node({x=0, y=-1, z=0}).name == "air" then
        -- Add a random block to the world
        local node = progression.block_list[math.random(1,allowed_block_level)]
        core.set_node({x=0, y=-1, z=0}, {name= node})

        -- Add a random entity to the block
        if allowed_entity_level > 0 then
            if math.random(1,100) > 90 then
                entity = progression.entity_list[math.random(1,allowed_entity_level)]
                core.add_item({x=0, y=0, z=0}, entity)
            end
        end
    end
end)

core.register_on_craft(function(itemstack, player, old_craft_grid, craft_inv)
    -- Called when `player` crafts something
    -- `itemstack` is the output
    -- `old_craft_grid` contains the recipe (Note: the one in the inventory is
    -- cleared).
    -- `craft_inv` is the inventory with the crafting grid
    -- Return either an `ItemStack`, to replace the output, or `nil`, to not
    -- modify it.

    -- Here select what the player is allowed to get in the one-block.
    local player_name = player:get_player_name()
    
    if itemstack:get_name() == "default:pick_wood" then
        allowed_block_level = 5
    elseif itemstack:get_name() == "default:pick_stone" then
        allowed_block_level = #progression.block_list
        allowed_entity_level = #progression.entity_list
    end
    player:set_attribute("allowed_block_level", allowed_block_level)
    player:set_attribute("allowed_entity_level", allowed_entity_level)  
    return nil
end)

