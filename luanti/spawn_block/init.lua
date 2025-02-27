local modname = core.get_current_modname()
local modpath = core.get_modpath(modname)
dofile(modpath .. DIR_DELIM .. "db.lua")
dofile(modpath .. DIR_DELIM .. "balance.lua")
local progression = dofile(modpath .. DIR_DELIM .. "progression.lua")
dofile(modpath .. DIR_DELIM .. "player_spawn.lua")

-- One_block game.
--   Initially the player will have access to only a few different blocks, like
--   dirt, and wood.
--   To progress the player must construct an idol and place it in the world.
--   A few idols needs to be constructed:
--    wood idol in the forest
--      punch the tree idol to get saplings and water
--    stone idol in a circle of stone close to an water source
--      punch the stone idol to get stone and lava
--    iron idol in a circle of iron blocks
--      punch the iron idol to get iron and coal
--    gold idol in a circle of gold blocks
--
--   As the game progresses certain entities will be made available to
--   the player when punching the various idols.  This could be a bucket with water
--   and lava to enable creating a stone factory or materials.

-- When the player digs the first block it returns itself and replaces it with a
-- randomly chosen block from the list of blocks available to the player at that time.
core.register_on_dignode(function(pos, oldnode, digger)
    if core.get_node({x=0, y=-1, z=0}).name == "air" then
        -- Game mode "number of blocks": Update world data and check if the player has progressed
        -- progression:check_progress_v2(digger)
        -- player_name = digger:get_player_name()
        -- core.chat_send_all(player_name .. " has dug " .. progression.blocks_dug .. " blocks")

        -- Add a random block to the world
        core.set_node({x=0, y=-1, z=0}, {name=progression:get_node()})

        -- Add a random entity to the block
        local entity = progression:get_entity()
        if entity then
            core.add_item({x=0, y=0, z=0}, entity)
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

    -- Game mode: Craft the right item. Here select what the player is allowed to get in the one-block.
    progression:check_progress(itemstack, player)
    return nil
end)
