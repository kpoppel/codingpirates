-- V.1: Wood idol must be crafted using wood blocks and the idol must be placed far enough from the origin.
--      the idol will message the player if it is satisfied with the location.
--      When the idol is placed correctly it will unlock the next level of blocks for the player.

-- Accept a variable when file loaded
local progression = ...

core.register_node("spawn_block_v3:idol_wood", {
    description = "Wooden Idol",
    tiles = {"wood_idol.png"},
    groups = {
        oddly_breakable_by_hand = 1,
        choppy = 2,
    },

    on_punch = function (pos, node, puncher, pointed_thing)
        -- Check if the player placed the idol far enough from the origin block
        local distance_to_origin = math.sqrt(pos.x^2 + pos.y^2 + pos.z^2)
        local minimum_distance = 50
        local player_name = puncher:get_player_name()
        if distance_to_origin >= minimum_distance then
            progression:check_progress_idols("wood", puncher)
            core.chat_send_player(player_name, "You hear a quiet humming, the wood idol is satisfied.")
            --core.chat_send_player(player_name, "Block level is now: " .. progression.allowed_block_level)
        else
            core.chat_send_player(player_name, "The idol does not seem to be satisfied with this location.  Maybe a bit further away?")
        end
    end,
})

core.register_craft({
    output = "spawn_block_v3:idol_wood",
    type = "shaped",
    recipe = {
        {            "", "default:tree",             ""},
        {"default:tree", "default:tree", "default:tree"},
        {"default:tree",             "", "default:tree"},
    }
})