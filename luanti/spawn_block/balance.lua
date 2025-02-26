local function list_check(p1, p2)
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
        if list_check(pos, {0,0,0}) then
            local nodes = core.find_nodes_in_area({x=-10,y=-10,z=-10}, {x=10,y=10,z=10}, {"default:tree","default:leaves"}, true)
            --core.chat_send_all("Found " .. #nodes["default:tree"] .. " trees")
            if nodes["default:tree"] and nodes["default:leaves"] then
                if #nodes["default:tree"] >= 8 and #nodes["default:leaves"] >= 60 then
                    core.chat_send_all("You did it!")
                    allowed_block_level = math.max(allowed_block_level,5)
                    local placement_list = {{x=pos.x+1,y=pos.y+1,z=pos.z+1},{x=pos.x+1,y=pos.y+1,z=pos.z},{x=pos.x+1,y=pos.y+1,z=pos.z-1},{x=pos.x,y=pos.y+1,z=pos.z+1},{x=pos.x,y=pos.y+1,z=pos.z-1},{x=pos.x-1,y=pos.y+1,z=pos.z+1},{x=pos.x-1,y=pos.y+1,z=pos.z},{x=pos.x-1,y=pos.y+1,z=pos.z-1}}

                    for i=1, #placement_list do
                        core.set_node(placement_list[i], {name= SList.bug[math.random(1,4)]})
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