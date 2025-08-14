-- V.1: Wood idol must be crafted using wood blocks and the idol must be placed far enough from the origin.
--      the idol will message the player if it is satisfied with the location.
--      When the idol is placed correctly it will unlock the next level of blocks for the player.
-- V.2: The wood idol requires some specific surrounings to be satisfied.
--      It will not be satisfied until it is placed in a forest with a minimum number of trees and leaves.
--      A standard tree has 8 wood blocks and 64 leaves.  Require 10 trees to call it a forest.
-- V.3: Add some 'bling' to the wood idol. Spawn some random butterflies and fireflies around the idol when it is placed correctly.
--      When punching the idol it gives back saplings to the player.
--      The idol cannot be dug up once placed in the place it likes.

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

                    -- Add some random butterflies and fireflies around the idol
                    local placement_list = {{x= 1, y=1,z= 1}, {x= 1,y=1,z= 0},
                                            {x= 1, y=1,z=-1}, {x= 0,y=1,z= 1},
                                            {x= 0, y=1,z=-1}, {x=-1,y=1,z= 1},
                                            {x=-1, y=1,z= 0}, {x=-1,y=1,z=-1}}

                    for _, p in pairs(placement_list) do
                        core.debug(dump({x=pos.x+p.x, y=pos.y+p.y, z=pos.z+p.z}))
                        core.debug(dump(SList.bug[math.random(1,4)]))
                        core.set_node({x=pos.x+p.x, y=pos.y+p.y, z=pos.z+p.z}, {name= SList.bug[math.random(1,4)]})
                    end
                    core.add_item({x=pos.x,y=pos.y+20,z=pos.z}, SList.sapling[math.random(1,9)])
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

    on_dig = function (pos, node, digger)
        core.chat_send_all("The Idol hums angrily, it will not move.")
    end
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

-- Ideas:
-- * Make the Idol harder to build by adding blocks for arms, legs, torso and head to build it (register_node and register_craft)
-- * Add sounds to the idol when it is placed correctly or incorrectly (core.play_sound)
-- * Add particles to the idol when it is placed correctly (core.add_particle)
-- * Check clock surroundings in on_place instead of every time it is punched.
--   Or add a flag to stop checking after correct placement.  Saving processing time.
-- * Have the idol use meshes instead of textures to make it look better in 3D.
-- * Make sure only one idol can be placed. (unregister craft?) Or player flag to only allow one idol. Set world metadata.