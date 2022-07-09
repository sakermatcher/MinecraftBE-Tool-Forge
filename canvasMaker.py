import numpy as np
from PIL import Image

originalIMG =(np.array(Image.open('C:/Users/juanp/AppData/Local/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/LocalState/games/forge/' + input('Img Name: ')+'.png')))
originalIMG = originalIMG.tolist()
canvas= []
for y in range(16):
    canvas.append([])
    for x in range(16):

        if originalIMG[y][x] == [0,0,0,0]:
            canvas[y].append(0)
        else:
            canvas[y].append(1)

print(str(canvas).replace('[', '\n['))
print(len(canvas))