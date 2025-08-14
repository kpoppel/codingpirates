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
        if check_pos(pos, {0,0,0}) then
            local nodes = core.find_nodes_in_area({x=-10,y=-10,z=-10}, {x=10,y=10,z=10}, {"default:tree","default:leaves"}, true)
            if nodes["default:tree"] and nodes["default:leaves"] then
                if #nodes["default:tree"] >= 8 and #nodes["default:leaves"] >= 60 then
                    core.chat_send_all("You did it!")
                    allowed_block_level = math.max(allowed_block_level,5)
                    local placement_list = {{x= 1, y=1,z= 1}, {x= 1,y=1,z= 0},
                                            {x= 1, y=1,z=-1}, {x= 0,y=1,z= 1},
                                            {x= 0, y=1,z=-1}, {x=-1,y=1,z= 1},
                                            {x=-1, y=1,z= 0}, {x=-1,y=1,z=-1}}

                    for _, p in pairs(placement_list) do
                        core.set_node({x=pos.x+p.x, x=pos.y+p.y, x=pos.z+p.z}, {name= SList.bug[math.random(1,4)]})
                    end
                    core.add_item({x=pos.x,y=pos.y+20,z=pos.z}, SList.sapling[math.random(1,9)])
                end
            else
                core.chat_send_all("Not enough trees")
            end
        end
    end,

    on_dig = function (pos, node, digger)
        core.chat_send_all("The Idol hums angrily")
    end
})

core.register_craftitem("oneblock:arm_wood", {
    description = "Wooden Arm"
})

core.register_craft({
    output = "oneblock:idol_wood",
    type = "shaped",
    recipe = {
        {"default:tree", "default:tree", "default:tree"},
        {"","",""},
        {"","",""},
    }
})