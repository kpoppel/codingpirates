-- V.1: Wood idol must be crafted using wood blocks and the idol must be placed far enough from the origin.
--      the idol will message the player if it is satisfied with the location.
--      When the idol is placed correctly it will unlock the next level of blocks for the player.
-- V.2: The wood idol requires some specific surrounings to be satisfied.
--      It will not be satisfied until it is placed in a forest with a minimum number of trees and leaves.
--      A standard tree has 8 wood blocks and 64 leaves.  Require 10 trees to call it a forest.
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
            -- Check if the idol is in a forest. If the trees are placed too close, there wil not be enough leaves!
            local require_trees = 1  -- <-- Set this one to how many treees you want to require
            local p1 = {x=pos.x-10,y=pos.y-10,z=pos.z-10}
            local p2 = {x=pos.x+10,y=pos.y+10,z=pos.z+10}
            local nodes = core.find_nodes_in_area(p1, p2, {"default:tree","default:leaves"}, true)
            --core.chat_send_player(player_name, dump(nodes))
            if nodes["default:tree"] and nodes["default:leaves"] then
                if #nodes["default:tree"] >= 8*require_trees and #nodes["default:leaves"] >= 60*require_trees then
                    progression:check_progress_idols("wood", puncher)
                    core.chat_send_player(player_name, "You hear a quiet humming, the wood idol is satisfied.")
                    --core.chat_send_player(player_name, "Block level is now: " .. progression.allowed_block_level)
                else
                    core.chat_send_player(player_name, "The idol tells you it likes forest.  Maybe some more trees would help?")
                end
            else
                core.chat_send_player(player_name, "The idol tells you the area is too barren.  Maybe some plants would help?")
            end
        else
            core.chat_send_player(player_name, "The idol does not seem to be satisfied with this location.  Maybe a bit further away?")
            core.add_item({x=pos.x,y=pos.y+20,z=pos.z}, "default:sapling")
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