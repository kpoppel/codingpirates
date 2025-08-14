on_dig = function (pos, node, digger)
    -- core.chat_send_all(tostring(progression.flags.wood_flag))
    if progression.flags.wood_flag then
        core.chat_send_all("The Idol hums angrily, it will not move.")
    else
        core.remove_node(pos)
        digger:get_inventory():add_item("main","oneblock_v2:idol_wood 1")
    end
end,