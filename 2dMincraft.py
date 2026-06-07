# A simple Minecraft-like game using Pygame
# version 1.0 with lancher. No new features will be added.
#lancher version 0.2
import json
import os
import time
world=input('Enter filename: ') + '.json'
running = True
if world == 'LAST.json':
    try:
        with open('LASTPLAYD.json', 'r') as f:
            world=json.load(f)['world']
    except FileNotFoundError:
        with open('LASTPLAYD.json', 'w') as f:
            json.dump({"world": world}, f)
import pygame
pygame.init()
pygame.mixer.init()
text_font = pygame.font.SysFont('Arial', 15)
hp=10
died=False
x=0
y=0
log=''
types=['grass','wood','planks']
types_textures = ['grass.png','wood.png','planks.png']
loaded_textures = []
pointer_couler=[(0,255,0),(150, 75, 0),(166, 123, 91)]
win = pygame.display.set_mode((500, 500))
direction = 1
texture_dir = 'GAME_TEXTURES'
save_dir='SAVES'
def get_texture_path(filename):
    path = os.path.join(texture_dir, filename)
    if os.path.isfile(path):
        return path
    return filename
missing_texture = None
def load_textures():
    global missing_texture
    loaded_textures.clear()
    missing_texture = pygame.image.load(get_texture_path('missing_texture.png')).convert_alpha()
    for i in types_textures:
        try:
            img = pygame.image.load(get_texture_path(i)).convert_alpha()
            loaded_textures.append(img)
        except Exception:
            loaded_textures.append(missing_texture.copy())  
def normalize_pointer_colors(pc, default_length=1):
    if isinstance(pc, dict):
        if all(str(key).isdigit() for key in pc.keys()):
            ordered = []
            for i in range(max(int(key) for key in pc.keys()) + 1):
                value = pc.get(str(i), pc.get(i))
                if isinstance(value, (list, tuple)) and len(value) == 3:
                    ordered.append(tuple(value))
                else:
                    ordered.append((0, 255, 0))
            return ordered
        pc = list(pc.values())
    if isinstance(pc, tuple):
        pc = [pc]
    if isinstance(pc, list):
        normalized = []
        for item in pc:
            if isinstance(item, (list, tuple)) and len(item) == 3:
                normalized.append(tuple(item))
        if normalized:
            return normalized
    return [(0, 255, 0)] * max(default_length, 1)
load_textures()
blocks = []
blobks_types = []
try:
    player_img = pygame.image.load(get_texture_path('player.png'))
except:
    text = text_font.render("Error: player.png not found.", True, (255, 0, 0))
    win.blit(text, (5, 200))
    pygame.display.update()
    time.sleep(5)
    running=False
try:
    with open(world, 'r') as f:
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
            pointer_couler= data['pc']
            correct_format = data['correct_format']
            try:
                types_textures = data['tc']
            except:
                types_textures = ['grass.png']
            pointer_couler = normalize_pointer_colors(data.get('pc', pointer_couler), len(types))
            lenoftypes = len(types)
            load_textures()
            if correct_format != ' 123ABC LOL IS THIS CORRECT?':
                raise KeyError
        except KeyError:
            blocks = []
            x = 0
            y = 0
            hp = 10
            win.fill((0, 0, 0))
            text = text_font.render(F"Error01: Invalid data format in {world}. Starting with default values.", True, (255, 0, 0))
            win.blit(text, (5,200))
            pygame.display.update()
            time.sleep(5)
            json.dump({"b": blocks,"bt": blobks_types, "X": x, "Y": y, "HP": hp, "d": direction, "correct_format": " 123ABC LOL IS THIS CORRECT?"}, open('blocks.json', 'w'))
except FileNotFoundError:
    blocks = []
    blobks_types = []
    with open(world, 'w') as f:
        text = text_font.render("No blocks.json found. Starting with default values.", True, (255, 0, 0))
        win.blit(text, (5, 200))
        pygame.display.update()
        time.sleep(5)
        json.dump({"b": blocks, "bt": blobks_types, "ty": types, "pc": pointer_couler, "X": x, "Y": y, "HP": hp, "d": direction, "correct_format": " 123ABC LOL IS THIS CORRECT?"}, f)
typeponter = 0
lenoftypes = len(types)
lix,liy=0,0
odd=True
while running:
    odd=True
    win.fill((0, 0, 0))
    win.blit(player_img, (x, y))
    walk_on=False
    pygame.draw.rect(win, (255, 255, 255), (0, 450, 500, 50))
    pygame.draw.rect(win, pointer_couler[typeponter], (0, 470, 20, 20))
    text=text_font.render(f'HP: {hp}', True, (0, 0, 255))
    text2=text_font.render(f'Block type: {types[typeponter]}', True, (0, 0, 255))
    win.blit(text, (30, 470))
    win.blit(text2, (100, 470))
    if direction == 0:lix,liy=x-50,y
    elif direction == 2:lix,liy=x,y-50
    elif direction == 1:lix,liy=x+50,y
    elif direction == 3:lix,liy=x,y+50
    pygame.draw.line(win, pointer_couler[typeponter], (x+25, y+25), (lix+25, liy+25), 2)
    p=0
    for block in blocks:
        try:
            texture = loaded_textures[types.index(blobks_types[p])]
            win.blit(texture, block)
        except (ValueError, IndexError):
            pygame.draw.rect(win, (255, 0, 255), (block[0], block[1], 50, 50))
        p+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x > 0 and (x-50,y) not in blocks:
                    x -= 50
                    walk_on=True
                direction = 0
            elif event.key == pygame.K_RIGHT:
                if x < 450 and (x+50,y) not in blocks:
                    x += 50
                    walk_on=True
                direction = 1
            elif event.key == pygame.K_UP:
                if y > 0 and (x,y-50) not in blocks:
                    y -= 50
                    walk_on=True
                direction = 2
            elif event.key == pygame.K_DOWN:
                if y < 400 and (x,y+50) not in blocks:
                    y += 50
                    walk_on=True
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
            if event.key == pygame.K_v:
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
with open(world, 'w') as f:
    data = {
        "b": blocks,
        "bt": blobks_types,
        "ty": types,
        'pc':pointer_couler,
        'X':x,
        'Y':y,
        'HP':hp,
        'd':direction,
        'tc':types_textures,
        'correct_format': ' 123ABC LOL IS THIS CORRECT?'
    }
    json.dump(data, f)
pygame.quit()
