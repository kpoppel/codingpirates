core.register_on_joinplayer(function(player)
    local name = player:get_player_name()
    core.set_node({x=0, y=-1, z=0}, {name= "default:dirt"})
    player:set_pos({x=0, y=0, z=0})
end)

local block_list = {
    "default:dirt",
    "default:stone",
    "default:dirt_with_grass",
    "default:tree"
}

-- local function random_elem(tb)
--     local keys = {}
--     for k in pairs(tb) do table.insert(keys, k) end
--     return tb[keys[math.random(#keys)]]
-- end

core.register_on_dignode(function(pos, oldnode, digger)
    --local node = random_elem(core.registered_nodes)
    local node = block_list[math.random(1,#block_list)]
    core.set_node({x=0, y=-1, z=0}, {name= node}) -- .name})
end)
































-- local S, PS = core.get_translator("hello")

-- -- on player spawn
-- core.register_on_joinplayer(function(player)
--     local name = player:get_player_name()
--     core.chat_send_player(name, S("Hello @1, how are you today?", name))
--     core.set_node({x=0, y=-1, z=0}, {name= "default:dirt"})
--     player:set_pos({x=0, y=0, z=0})
-- end)

-- core.register_chatcommand("playtime", {
--     func = function(name)
--         local last_login = core.get_auth_handler().get_auth(name).last_login
--         local playtime = math.floor((last_login-os.time())/60)
--         return true, PS(
--             "You have been playing for @1 minute.",
--             "You have been playing for @1 minutes.",
--             minutes, tostring(minutes))
--     end,
-- })

-- minetest.register_on_newplayer(function(player)
-- 	on_spawn(player, true)
-- end)

-- minetest.register_on_respawnplayer(function(player)
-- 	return on_spawn(player, false)
-- end)

-- -- Register a function to be called after the world is generated
-- core.register_on_worldgen_done(function()
--     -- Get the player's initial spawn position.  This is a bit tricky,
--     -- as the player hasn't *actually* spawned yet.  We have to get
--     -- it from the world generation settings.
--     local spawn_pos = core.settings:get_pos("spawn_point")

--     -- Check if a spawn point is defined. If not, default to 0,0,0
--     if spawn_pos == nil then
--         spawn_pos = {x=0, y=0, z=0}
--     end

--     -- Calculate the position of the block *below* the spawn point.
--     local block_pos = {x = spawn_pos.x, y = spawn_pos.y - 1, z = spawn_pos.z}

--     -- Check if there is already a node there. If so, don't do anything.
--     if core.get_node(block_pos).name == "air" then
--         -- Set the node to whatever block you want.  "default:dirt" is a good
--         -- choice, but you could use anything.
--         core.set_node(block_pos, {name = "default:dirt"})
--     end


--     -- Optional:  Add a message to the server log to confirm the block placement.
--     core.log("action", "Placed support block at " .. core.pos_to_string(block_pos))

-- end)


-- -- Optional: A chat command to reset the spawn point.  Useful for testing.
-- core.register_chatcommand("/resetspawn", {
--     func = function(name, param)
--         local pos = core.string_to_pos(param)
--         if pos then
--             core.settings:set("spawn_point", pos)
--             core.chat_send_all("Spawn point set to " .. param)
--         else
--             core.chat_send_player(name, "Usage: /resetspawn x,y,z")
--         end
--     end
-- })