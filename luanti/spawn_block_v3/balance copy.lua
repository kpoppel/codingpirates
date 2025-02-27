-- First version of the balance theme: creating idols in the world with certain
-- surroundings is a sign of harmony with the environment.
-- The first version is a simple implementation of the wood idol.
-- The player must construct a wooden idol in the forest by placing a tree block in the crafting grid.

local function check_pos(p1, p2)
    -- Utility function to compare two positions, one {x=,y=,z=} and the other {x,y,z}
    return p1.x == p2[1] and p1.y == p2[2] and p1.z == p2[3]
end

core.register_node("oneblock:idol_wood", {
    description = "Wooden Idol",
    tiles = {"wood_idol.png"},
    groups = {
        oddly_breakable_by_hand = 1,
        choppy = 2,
    },

    on_punch = function (pos, node, puncher, pointed_thing)
        -- Ceheck if the player place the idol far enough from the origin block
        local distance_to_origin = math.sqrt(pos.x^2 + pos.y^2 + pos.z^2)
        local minimum_distance = 50
        if distance_to_origin >= minimum_distance then
            local p1 = {x=-10,y=-10,z=-10}
            local p2 = {x=10,y=10,z=10}
            local nodes = core.find_nodes_in_area(p1, p2, {"default:tree","default:leaves"}, true)
            if nodes["default:tree"] and nodes["default:leaves"] then
                if #nodes["default:tree"] >= 8 and #nodes["default:leaves"] >= 60 then
                    core.chat_send_all("You hear a quiet humming, the wood idol is satisfied.")
                    progression:check_progress_idols("wood")
                end
            end
        end
    end,
})

core.register_craft({
    output = "oneblock:idol_wood",
    type = "shaped",
    recipe = {
        {            "", "default:tree",             ""},
        {"default:tree", "default:tree", "default:tree"},
        {"default:tree",             "", "default:tree"},
    }
})

