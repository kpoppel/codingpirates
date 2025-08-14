-- VERSION 1 - wood and stone pickaxes
-- This file contains lists of blocks and entities that can be spawned in the world.
-- The blocks are used to replace the block under the player when dug.
-- As the game progresses more blocks are made available to the player.

local Progression = {
    block_list = {
        -- block level 1
        "default:dirt",
        "default:tree",
        "default:dirt_with_grass",
    
        -- block level 2 - after wood pickaxe
        "default:stone",
        "default:leaves",
    },

    entity_list = {
        "bucket:bucket_water",
        "bucket:bucket_lava",
    },

    allowed_block_level = 3,
    allowed_entity_level = 0,

    check_progress = function(self, itemstack, player)
        -- Check player level and crafting level
         -- Load the allowed_block_level from the player's metadata
        local player_block_level = player:get_attribute("allowed_block_level")
        local player_entity_level = player:get_attribute("allowed_entity_level")

        if saved_block_level then
            self.allowed_block_level = math.max(self.allowed_block_level, tonumber(saved_block_level))
        end
    
        if saved_entity_level then
            self.allowed_entity_level = math.max(self.allowed_entity_level, tonumber(saved_entity_level))
        end

        -- Check the level based on what the player crafted
        if itemstack:get_name() == "default:pick_wood" then
            self.allowed_block_level = math.max(self.allowed_block_level,5)
            self.allowed_entity_level = 0
        elseif itemstack:get_name() == "default:pick_stone" then
            self.allowed_block_level = math.max(self.allowed_block_level,#self.block_list)
            self.allowed_entity_level = #self.entity_list
        end
        player:set_attribute("allowed_block_level", self.allowed_block_level)
        player:set_attribute("allowed_entity_level", self.allowed_entity_level)
    end,

    get_node = function(self)
        return self.block_list[math.random(1,self.allowed_block_level)]
    end,

    get_entity = function(self)
        if math.random(1,100) > 90 then
            return self.block_list[math.random(1,self.allowed_entity_level)]
        else
            return nil
        end
    end,
}

return Progression
-- End of spawn_block/progression.lua