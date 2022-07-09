from string import capwords
from PIL import Image
import numpy as np
from blend_modes import multiply, normal
from helper.variables.canvas import canvas
from helper.variables.jsons import *
import json

with open (r'C:\Users\juanp\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\forge\materials.json') as materials:
    configDict= json.load(materials)#Convert the json containing the paths and the materials to a dict

newGenRP= configDict['paths']['newStuff']+'resources/'
newGenBP= configDict['paths']['newStuff']+'behavior/'
minecraftToolsFolderRP = configDict['paths']['myResources'] + 'textures/items/tools/'
minecraftToolsFolderBP = configDict['paths']['myBehavior'] + 'items/tools/'
molds= configDict['paths']['molds']

for i in [newGenBP+'checkhand.txt', newGenRP+'item_texture.txt']:
    with open (i, 'w+') as writer:#Empty checkhand.txt and item_texture.txt so that there are no duplicates
        writer.write('')

rodCleaner=[]#This is a list containing which pixels should be deleted from a rod when transformed to a tool
for y in range(16):
    for x in range(16):
        if canvas['rodDeleter'][y][x] == 1:
            rodCleaner.append([y,x])



class material:#Define a new material
    def __init__(self, name, speed, durability, RGBA, speedMultiplier, durabilityMultiplier, repairItems, miningLVL, family, modifier, extraInfo=[]):
        self.name= name
        self.RGBA= tuple(RGBA)
        self.speed= speed
        self.durability= durability
        self.sMultiplier= speedMultiplier
        self.dMultiplier= durabilityMultiplier
        self.repairItems= repairItems
        self.miningLVL= miningLVL
        self.family= family
        self.EI= extraInfo

        {'none':'do nothing'}[modifier]#Run a modifier function by searching it on the dictionary
    
class modifiers:
    def none():
        pass

def textureMaker(path, RGBA, Canvas, opacity=0.7): #Blends a base texture with a meterial's color
    colorIMGlist =[]#Create a List with transparent RGBA values based on the Canvas size and place the RGBA colors were there is a one on canvas
    for y in range(len(canvas[Canvas])):
        colorIMGlist.append([])
        for x in range(len(canvas[Canvas][y])):
            if canvas[Canvas][y][x]==1: #One on Canvas
                colorIMGlist[y].append (RGBA)#Color the pixel 
            else: #0 on Canvas
                colorIMGlist[y].append((0,0,0,0)) #transparent RGBA

    colorIMG = np.array(colorIMGlist)#Make the list created above an np.array
    moldIMG= np.array(Image.open(molds +Canvas+ '.png'))#Find the base texture or the mold by name (the image's name has to be the same as the canvas' name)

    moldIMGfloat = moldIMG.astype(float)#Values need to be floats to use the blend module
    colorIMGfloat= colorIMG.astype(float)#Values need to be floats to use the blend module

    blendedImgFloat= multiply(colorIMGfloat, moldIMGfloat, opacity) #Blend images
    blendedImg= np.uint8(blendedImgFloat) #Convert the floats back to ints 
    blendedResult= Image.fromarray(blendedImg) #Convert array format to image format
    blendedResult.save(path+'.png') #Save image




def textureBlender(path, originalPaths, deleter=[]):#Layers images on top of each order
    originalIMGs=[]
    for i in originalPaths: #Find every image in originalPaths and convert it to an array and to a float
        originalIMGs.append(np.array(Image.open(i+'.png')).astype(float))

    blendedImgFloat= normal(originalIMGs[0], originalIMGs[1], 1.0) #Blend the first two images
    if len(originalIMGs) > 2: #If there is more than two images combine the remaining
        for i in range (len(originalIMGs)-2):
            blendedImgFloat= normal(blendedImgFloat.copy(), originalIMGs[i+2], 1.0)
    
    blendedImg= np.uint8(blendedImgFloat) #Convert the floats back to ints 
    for i in deleter:#Use delater to delate any unwanted pixels
        blendedImg[i[0],i[1]]= (0,0,0,0)
    blendedResult= Image.fromarray(blendedImg) #Convert array format to image format
    blendedResult.save(path+'.png') #Save image




def forge(selector= ['all']):
    global materialsPerFamily
    selections = {'pick':{'resources': pickResources, 'behavior':pickBehavior}}#Select if you want to forge only a specific part or all (This dict contains all possible selections)
    if selector[0] == 'all': #Forge all
        for i in selections.values():
            for l in i.values():
                x=l()
    else: #Specific Forge
        if selector[1] == 'all':#Forge resources and behavior for the specified tool
            for i in selections[selector[0]].values():
                x=i()
        else: #Forge the specified side (Behavior or Resources) for the specified tool
            for i in range(len(selector)-1):
                x=list(selections[selector[0]].values())[i]()

def  pickResources():
    for fam in materialsPerFamily:#Go thru every family
        for mat in fam:#Go thru every material inside the family
            toDo= ['head']
            if "prerod" not in mat.EI: #Check if there is a preset rod for that material
                toDo.append('rod') #Add rod to the material toDo

                if fam.index(mat) != 0: #Add sharpening to my toDo if its not for the first material in the family

                    toDo.append('sharpening')

            for part in toDo:#Create a head and rod or only a head depending on the above for that material
                textureMaker(f'{newGenRP}parts/{part}/{mat.name}', mat.RGBA, part)#Make the texture]

                with open(newGenRP+'item_texture.txt', 'a') as writer:
                    writer.write( ',\n' + f'"{mat.name}_{part}":' + json.dumps({"textures":f'textures/items/tools/parts/{part}/{mat.name}'}, indent=4))


        for rod in fam:#Cycle every possible pickaxe combination
            for head in fam:
                if "prerod" not in rod.EI:
                    #Blend the textures using the newly made rod
                    textureBlender(newGenRP+'pickaxe/'+ f'fam{head.family}/{head.name}_{rod.name}', [newGenRP + f'parts/rod/{rod.name}', newGenRP + f'parts/head/{head.name}'], rodCleaner)
                else:
                    #Blend the textures using the allready made rod
                    textureBlender(newGenRP+'pickaxe/'+ f'fam{head.family}/{head.name}_{rod.name}', [minecraftToolsFolderRP + f'parts/rod/{rod.name}', newGenRP + f'parts/head/{head.name}'], rodCleaner)
                
                with open(newGenRP+'item_texture.txt', 'a') as writer:
                    writer.write( ',\n' + f'"{head.name}_{rod.name}_pickaxe":' + json.dumps({"textures":f'textures/items/tools/pickaxe/fam{head.family}/{head.name}_{rod.name}'}, indent=4))

                #Make a version of the tool with paper
                for sharpening in fam[fam.index(head)+1:]:
                    #Make sharpened pickaxes
                    textureBlender(newGenRP+'pickaxe/'+ f'fam{head.family}/sharpened/{head.name}_{rod.name}_{sharpening.name}', [newGenRP+ f'pickaxe/fam{head.family}/{head.name}_{rod.name}', newGenRP + f'parts/sharpening/{sharpening.name}'])
                    with open(newGenRP+'item_texture.txt', 'a') as writer:
                        writer.write( ',\n' + f'"{head.name}_{rod.name}_{sharpening.name}_pickaxe":' + json.dumps({"textures":f'textures/items/tools/pickaxe/fam{head.family}/sharpened/{head.name}_{rod.name}_{sharpening.name}'}, indent=4))

                #Make the paper pickaxes
                textureBlender(newGenRP+'pickaxe/'+ f'fam{head.family}/{head.name}_{rod.name}_paper', [newGenRP+ f'pickaxe/fam{head.family}/{head.name}_{rod.name}', minecraftToolsFolderRP + 'parts/addups/paper'])
                with open(newGenRP+'item_texture.txt', 'a') as writer:
                    writer.write( ',\n' + f'"{head.name}_{rod.name}_paper_pickaxe":' + json.dumps({"textures":f'textures/items/tools/pickaxe/fam{head.family}/{head.name}_{rod.name}_paper'}, indent=4))

 

def pickBehavior():
    for fam in materialsPerFamily:
        for mat in fam:
            toDo = ['rod', 'head']
            if fam.index(mat) != 0: #Add sharpening to my toDo if its not for the first material in the family
                    toDo.append('sharpening')
            for part in toDo:
                #Make the behavior for the individual parts
                part2=part
                if part == 'sharpening':#This is only because sharpening is named sharpening kit but the path and identifier use only sharpening
                    part2= 'Sharpening Kit'
                itemCreator(newGenBP+f'parts/{part}/', f'sak:{mat.name}_{part}', capwords(f'{mat.name} {part2}')+ f'\n§bFamily: {mat.family}')

        for rod in fam:
            for head in fam:
                #Make the behavior for the non sharpened pickaxes
                toolCreator('pickaxe', capwords(f'{head.name} and {rod.name}') + '\n§bPickaxe', f'sak:{head.name}_{rod.name}_pickaxe', int(head.durability*rod.dMultiplier), list(dict.fromkeys(head.repairItems + rod.repairItems)), round(head.speed*rod.sMultiplier, 2), head.miningLVL, [], newGenBP+f'pickaxe/fam{head.family}/', newGenBP)
                #Make the behavior for the paper pickaxes
                toolCreator('pickaxe', capwords(f'{head.name} and {rod.name}') + f'\n§b{capwords("paper binded pickaxe")}', f'sak:{head.name}_{rod.name}_paper_pickaxe', int(head.durability*rod.dMultiplier), list(dict.fromkeys(head.repairItems + rod.repairItems + ['minecraft:paper'])), round(head.speed*rod.sMultiplier, 2), head.miningLVL, [], newGenBP+f'pickaxe/fam{head.family}/', newGenBP)

                for sharpening in fam[fam.index(head)+1:]:
                    #Make the behavior for the sharpened pickaxes 
                    toolCreator('pickaxe', capwords(f'{head.name} and {rod.name}') + f'\n§b{capwords(sharpening.name + " pointed pickaxe")}', f'sak:{head.name}_{rod.name}_{sharpening.name}_pickaxe', int(head.durability*rod.dMultiplier), list(dict.fromkeys(head.repairItems + rod.repairItems)), round(head.speed*rod.sMultiplier, 2), sharpening.miningLVL, [], newGenBP+f'pickaxe/fam{head.family}/sharpened/', newGenBP)
                

#Material Setup

materialsPerFamily = [[]]#Materials ordered in their own families

for families in range(1, len(configDict['families'].values())):#Convert the materials from materials.json into classes and order them by family
    materialsPerFamily.append([])
    for mat in configDict['families'][str(families)]:
        materialsPerFamily[families].append(material(mat['name'], mat['head']['speed'], mat['head']['durability'], mat['RGBA'], mat['rod']['speedMultiplier'], mat['rod']['durabilityMultiplier'], mat['baseItemIDs'], mat['head']['miningLVL'], families, mat['modifier'], mat['extraInfo']))

forge()#Startup