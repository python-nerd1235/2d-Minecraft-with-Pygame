# A simple Minecraft-like game using Pygame
# version 0.5 Texture update!
import pygame
import json
import time
pygame.init()
text_font = pygame.font.SysFont('Arial', 20)
hp=10
died=False
x=0
y=0
log=''
types=[(0, 255, 0)]
types_texures = ['grass.png']
loaded_textures = []
types_text=['Grass']
win = pygame.display.set_mode((500, 500))
direction = 1
for i in types_texures:
    try:
        img = pygame.image.load(i)
        loaded_textures.append(img)
    except:
        loaded_textures.append('missing_texture.png')
blocks = []
blobks_types = []
running = True
try:player_img = pygame.image.load('player.png')
except:
    text = text_font.render("Error: player.png not found.", True, (255, 0, 0))
    win.blit(text, (5, 200))
    pygame.display.update()
    time.sleep(5)
    running=False
try:
    with open('blocks.json', 'r') as f:
        data = json.load(f)
        print(data)
        if isinstance(data, list):
            data = data[0]
        try:
            a = data['b']
            for i in a:
                blocks.append((i[0], i[1]))
            x = data['X']
            y = data['Y']
            hp = data['HP']
            blobks_types = data['bt']
            types = data['ty']
            direction = data['d']
            correct_format = data['correct_format']
            if correct_format != ' 123ABC LOL IS THIS CORRECT?':
                raise KeyError
        except KeyError:
            blocks = []
            x = 0
            y = 0
            hp = 10
            win.fill((0, 0, 0))
            text = text_font.render("Error: Invalid data format in blocks.json. Starting with default values.", True, (255, 0, 0))
            win.blit(text, (5,200))
            pygame.display.update()
            time.sleep(5)
            json.dump({"b": blocks,"bt": blobks_types, "X": x, "Y": y, "HP": hp, "d": direction, "correct_format": " 123ABC LOL IS THIS CORRECT?"}, open('blocks.json', 'w'))
except FileNotFoundError:
    blocks = []
    blobks_types = []
    with open('blocks.json', 'w') as f:
        text = text_font.render("No blocks.json found. Starting with default values.", True, (255, 0, 0))
        win.blit(text, (5, 200))
        pygame.display.update()
        time.sleep(5)
        json.dump({"b": blocks, "bt": blobks_types, "ty": [(0, 255, 0)], "X": x, "Y": y, "HP": hp, "d": direction, "correct_format": " 123ABC LOL IS THIS CORRECT?"}, f)
typeponter = 0
lenoftypes = len(types)
lix,liy=0,0
odd=True
while running:
    odd=True
    win.fill((0, 0, 0))
    win.blit(player_img, (x, y))
    pygame.draw.rect(win, (255, 255, 255), (0, 450, 500, 50))
    pygame.draw.rect(win, types[typeponter], (0, 470, 20, 20))
    text=text_font.render(f'HP: {hp}', True, (0, 0, 255))
    text2=text_font.render(f'Block type: {types_text[typeponter]}', True, (0, 0, 255))
    win.blit(text, (30, 470))
    win.blit(text2, (100, 470))
    if direction == 0:lix,liy=x-50,y
    elif direction == 2:lix,liy=x,y-50
    elif direction == 1:lix,liy=x+50,y
    elif direction == 3:lix,liy=x,y+50
    pygame.draw.line(win, types[typeponter], (x+25, y+25), (lix+25, liy+25), 2)
    p=0
    for block in blocks:
        win.blit(loaded_textures[types.index(blobks_types[p])], block)
        p+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x > 0 and (x-50,y) not in blocks:
                    x -= 50
                direction = 0
            elif event.key == pygame.K_RIGHT:
                if x < 450 and (x+50,y) not in blocks:
                    x += 50
                direction = 1
            elif event.key == pygame.K_UP:
                if y > 0 and (x,y-50) not in blocks:
                    y -= 50
                direction = 2
            elif event.key == pygame.K_DOWN:
                if y < 400 and (x,y+50) not in blocks:
                    y += 50
                direction = 3
            elif event.key == pygame.K_d:
                hp -= 1
            elif event.key == pygame.K_c:
                direction = (direction + 1) % 4
            if event.key == pygame.K_x:       #where the player can remove blocks
                if direction == 0 and (x-50,y) in blocks:
                    idx = blocks.index((x-50,y))
                    blocks.pop(idx)
                    blobks_types.pop(idx)
                elif direction == 1 and (x+50,y) in blocks:
                    idx = blocks.index((x+50,y))
                    blocks.pop(idx)
                    blobks_types.pop(idx)
                elif direction == 2 and (x,y-50) in blocks:
                    idx = blocks.index((x,y-50))
                    blocks.pop(idx)
                    blobks_types.pop(idx)
                elif direction == 3 and (x,y+50) in blocks:
                    idx = blocks.index((x,y+50))
                    blocks.pop(idx)
                    blobks_types.pop(idx)
            if event.key == pygame.K_z:
                if direction == 0 and (x - 50, y) not in blocks:      #where the player can place blocks
                    blocks.append((x - 50, y))
                    blobks_types.append(types[typeponter])
                elif direction == 1 and (x + 50, y) not in blocks:
                    blocks.append((x + 50, y))
                    blobks_types.append(types[typeponter])
                elif direction == 2 and (x, y - 50) not in blocks:
                    blocks.append((x, y - 50))
                    blobks_types.append(types[typeponter])
                elif direction == 3 and (x, y + 50) not in blocks:
                    blocks.append((x, y + 50))
                    blobks_types.append(types[typeponter])
            if event.key == pygame.K_SPACE:
                typeponter = (typeponter + 1) % lenoftypes
    if hp <= 0:
        died=True
        running=False
    pygame.display.update()
    pygame.time.Clock().tick(30)
print("Thanks for playing!")
if died:
    win.fill((0, 0, 0))
    hp=10
    text = text_font.render("You died!", True, (255, 0, 0))
    win.blit(text, (200, 200))
    pygame.display.update()
    pygame.time.wait(2000)
with open('blocks.json', 'w') as f:
    data = {
        "b": blocks,
        "bt": blobks_types,
        "ty": types,
        'X':x,
        'Y':y,
        'HP':hp,
        'd':direction,
        'correct_format': ' 123ABC LOL IS THIS CORRECT?'
    }
    json.dump(data, f)
pygame.quit()
