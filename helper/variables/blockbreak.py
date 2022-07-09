blockbreakingDict = {
    'pickaxe': {

        'default': {
            0: ["stone", "cobblestone", "double_stone_slab", "stone_slab", "mossy_cobblestone", "stone_stairs", "stone_pressure_plate", "stone_button", "stonebrick", "stone_brick_stairs", "stonecutter", "stone_slab4", "granite_stairs", "diorite_stairs", "andesite_stairs", "polished_granite_stairs", "polished_diorite_stairs", "polished_andesite_stairs", "mossy_stone_brick_stairs", "mossy_cobblestone_stairs", "normal_stone_stairs", "smooth_stone", "grindstone", "stonecutter_block", "lodestone", "cobblestone_wall", ],  # Wooden Pickaxeo
            1: [],
            2: ["pointed_dripstone", "dripstone_block", "sandstone", "sandstone_stairs", "smooth_sandstone_stairs", ],
            3: ["candle", "white_candle", "yellow_candle", "netherrack", "nether_brick", "nether_brick_fence", "nether_brick_stairs"],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
            15: [],
        },

        'custom': {
            0: [],
            1: [],
            2: ["sak:osmium_ore", "sak:osmium_block"],
            3: ["sak:tin_ore", "sak:tin_block"],
            4: [],
            5: ["sak:silver_ore", "sak:silver_block"],
            6: [],
            7: ["sak:lead_ore", "sak:lead_block"],
            8: ["sak:nickel_ore", "sak:nickel_block"],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
            15: ["sak:platinum_ore", "sak:platinum_block"]
        }
    },
    'axe': {
        'default': {
            0: ["log", "planks", "bed", "oak_stairs", "chest", "crafting_table", "standing_sign", "wooden_door", "ladder", "wall_sign", "wooden_pressure_plate", "fence", "trapdoor", "fence_gate", "spruce_stairs", "birch_stairs", "jungle_stairs", "trapped_chest", "double_wooden_slab", "wooden_slab", "standing_banner", "wall_banner", "spruce_fence_gate", "birch_fence_gate", "jungle_fence_gate", "spruce_door", "birch_door", "jungle_door", "stripped_spruce_log", "stripped_birch_log", "stripped_jungle_log", "stripped_oak_log", "birch_button", "jungle_button", "spruce_button", "birch_trapdoor", "jungle_trapdoor", "spruce_trapdoor", "birch_pressure_plate", "jungle_pressure_plate", "spruce_pressure_plate", "spruce_standing_sign", "spruce_wall_sign", "birch_standing_sign", "birch_wall_sign", "jungle_standing_sign", "jungle_wall_sign", "lectern", "cartography_table", "fletching_table", "barrel", "loom", "composter", "wood", "cocoa", ],  # Bone Axe
            1: [],
            2: [],
            3: ["candle_cake", "white_candle_cake", "yellow_candle_cake"],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
            15: []
        }
    },
    'shovel': {
        'default': {
            0: ["gravel"],  # Paper Shovel
            1: ["sand"],
            2: ["mud"],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
            15: []
        }
    }
}


def breaking(tool, speed, LVL) -> list:
    blockBreakingList = []
    for toolLists in list(blockbreakingDict[tool]['default'].values())[:LVL+1]:
        for block in toolLists:
            blockBreakingList.append({
                "block": 'minecraft:'+block,
                "speed": speed,
                "on_dig":  {"event":"break"}

            })

    for toolLists in list(blockbreakingDict[tool]['default'].values())[LVL+1:]:
        for block in toolLists:
            blockBreakingList.append({
                "block": 'minecraft:'+block,
                "speed": 0,
                "on_dig":  {"event":"break"}
            })
    toolset= ['pickaxe', 'axe', 'shovel']
    toolset.remove(tool)
    for notTool in toolset:
        for toolLists in list(blockbreakingDict[notTool]['default'].values()):
            for block in toolLists:
                blockBreakingList.append({
                    "block": 'minecraft:'+block,
                    "speed": 0,
                    "on_dig":  {"event":"break"}

                })
    return blockBreakingList
