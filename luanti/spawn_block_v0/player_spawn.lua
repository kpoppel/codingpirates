-- Player spawning.
-- If a new player joins place a block under the player if there is air in that space.
-- If a player joins again, just place the player on the block.
local function on_spawn(player, is_newplayer)
    local name = player:get_player_name()
    --if core.get_node({x=0, y=-1, z=0}).name == "air" then
    core.set_node({x=0, y=-1, z=0}, {name= "default:dirt"})
    --end
    if is_newplayer then
        core.chat_send_player(name, "Welcome to oneblock!  Don't fall down!")
    end
    player:set_pos({x=0, y=0, z=0})
end

core.register_on_newplayer(function(player)
    on_spawn(player, true)
end)

core.register_on_joinplayer(function(player)
    -- Load the allowed_block_level from the player's metadata
    local player_name = player:get_player_name()
    local saved_block_level = player:get_attribute("allowed_block_level")
    local saved_entity_level = player:get_attribute("allowed_entity_level")

    if saved_block_level then
        allowed_block_level = tonumber(saved_block_level)
    end

    if saved_entity_level then
        allowed_entity_level = tonumber(saved_entity_level)
    end

    -- Then do the spawn
    on_spawn(player, false)
end)

-- Ensure that if a player falls off the platform it is re-sent to the one block spot.
local function get_all_player_names()
    local players = core.get_connected_players()
    local player_names = {}
    for _, player in ipairs(players) do
        table.insert(player_names, player:get_player_name())
    end
    return player_names
end

local function check_player_position()
    local player_names = get_all_player_names()
    for _, name in ipairs(player_names) do
        local player = core.get_player_by_name(name)
        if player then
            local pos = player:get_pos()
            if pos.y < -100 then
                core.chat_send_player(name, "OH NO, you fell off the world!!")
                on_spawn(player, false)
            end
        end
    end
end

local timer = 0
core.register_globalstep(function(dtime)
    timer = timer + dtime
    if timer >= 1 then
        check_player_position()
        timer = 0
    end
end)