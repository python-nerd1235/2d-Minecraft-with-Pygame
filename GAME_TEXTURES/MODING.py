#2d mincraft mod maker 
#ver 1.0_B
#game at: https://github.com/python-nerd1235/2d-Minecraft-with-Pygame/tree/main
import json
names=['grass']
coulers={
    'red':(255,0,0),
    'blue':(0,0,255),
    'green':(0,255,0)
}
files=['grass.png']
couler=[(0,255,0)]
run=True
while run:
    a=input('enter the name of the block: ')
    names.append(a)
    a=input('enter the couler: ')
    couler.append(coulers[a])
    a=input('enter the name of the texture: ')
    files.append(a)
    if input('Quit?y/n: ')=='y':
        run = False
with open(input('enter the name of your mod: ')+'.json', 'w') as f:
    data = {
        "b": [],
        "bt": [],
        "ty": names,
        'pc':coulers,
        'X':0,
        'Y':0,
        'HP':10,
        'd':1,
        'tc':files,
        'correct_format': ' 123ABC LOL IS THIS CORRECT?'
    }
    json.dump(data, f)