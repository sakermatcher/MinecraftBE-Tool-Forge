from helper.variables.blockbreak import breaking
import json

def toolCreator(tool:str, name: str, identifier: str, durability: int, repairItems: list, speed: int, miningLVL: int, commands: list, path:str, checkHandPath:str):

    JSON = {
        "format_version": "1.17.0",
        "minecraft:item": {
            "description": {
                "identifier": identifier,
                "category": "commands"
            },
            "components": {
                "minecraft:hand_equipped": True,
                "minecraft:max_stack_size": 1,
                "minecraft:display_name": {
                    "value": name + f'\n§eSPEED: {speed}\n§7DURABILITY: {durability}\n§aMINING LVL: {miningLVL}'
                },
                "minecraft:icon": {
                    "texture": identifier[4:]
                },
                "minecraft:damage": 2,
                "minecraft:enchantable": {
                    "slot": "pickaxe",
                    "value": 5
                },
                "minecraft:can_destroy_in_creative": True,
                "minecraft:durability": {
                    "max_durability": durability
                },
                "minecraft:repairable": {
                    "repair_items": [
                        {
                            "repair_amount": int(durability/3),
                            "items": repairItems
                        }
                    ]
                },
                "minecraft:digger": {
                    "use_efficiency": True,
                    "on_dig": {
                        "event": "break"
                    },
                    "destroy_speeds": breaking(tool, speed, miningLVL)
                }
            },
            "events": {
                "break": {
                    "sequence": [
                        {"damage": {
                            "type": "magic",
                            "amount": 1,
                            "target": "self"
                        }},
                        {"run_command": {
                            "command": commands,
                            "target": "self"
                        }}
                    ]}
            }
        }}

    JSONWriter(path+f'{identifier[4:]}', JSON)

    
    with open(checkHandPath + "checkhand.txt", 'a') as writer:
        writer.write('tag @a [hasitem={item='+identifier+', location=slot.weapon.mainhand}] remove notool\n')

def itemCreator(path:str, identifier:str, name:str, stack=64):
    JSON = {
        "format_version": "1.17.0",
        "minecraft:item": {
            "description": {
                "identifier": identifier,
                "category": "items"
            },
            "components": {
                "minecraft:hand_equipped": False,
                "minecraft:max_stack_size": stack,
                "minecraft:display_name": {
                    "value": name
                },
                "minecraft:icon": {
                    "texture": identifier[4:]
                },
                
                "minecraft:can_destroy_in_creative": True
            },
            "events": {
            }
        }}

    JSONWriter(path+f'{identifier[4:]}', JSON)


furRecipeDict = {
    "format_version": "1.12",
    "minecraft:recipe_furnace": {
        "description": {
            "identifier": ""
        },


        "tags": ["furnace", "blast_furnace"],
        "input": "",
        "output": ""
    }
}

def JSONWriter(path, JSON):
    with open(path+'.json', 'w+', ) as writer:
        writer.write(json.dumps(JSON, indent=4))