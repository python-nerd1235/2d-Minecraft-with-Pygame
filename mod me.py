# A simple Minecraft-like game using Pygame
# version 0.3_A
import pygame
import json
pygame.init()
text_font = pygame.font.SysFont('Arial', 20)
hp=10
died=False
x=0
y=0
log=''
win = pygame.display.set_mode((500, 500))
direction = 1
blocks = []
try:
    with open('blocks.json', 'r') as f:
        data = json.load(f)
        print(data)
        if isinstance(data, list):
            data = data[0]
        try:
            blocks = data['b']
            x = data['X']
            y = data['Y']
            hp = data['HP']
            direction = data['d']
        except KeyError:
            blocks = []
            x = 0
            y = 0
            hp = 10
            print("Invalid data format in blocks.json. Starting with default values.")
            json.dump({"b": blocks, "X": x, "Y": y, "HP": hp}, open('blocks.json', 'w'))
except FileNotFoundError:
    blocks = []
    with open('blocks.json', 'w') as f:
       json.dump({"b": blocks, "X": x, "Y": y, "HP": hp, "dir": direction}, f)
types=[(0, 255, 0)]
typeponter = 0
lenoftypes = len(types)
lix,liy=0,0
odd=True
running = True
while running:
    odd=True
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 255, 0), (x, y, 50, 50))
    pygame.draw.rect(win, (255, 255, 255), (0, 450, 500, 50))
    pygame.draw.rect(win, types[typeponter], (0, 470, 20, 20))
    text=text_font.render(f'HP: {hp}', True, (0, 0, 255))
    win.blit(text, (30, 470))
    if direction == 0:lix,liy=x-50,y
    elif direction == 2:lix,liy=x,y-50
    elif direction == 1:lix,liy=x+50,y
    elif direction == 3:lix,liy=x,y+50
    pygame.draw.line(win, types[typeponter], (x+25, y+25), (lix+25, liy+25), 2)
    for block in blocks:
        if odd:
            pygame.draw.rect(win, types[0], (block[0], block[1], 50, 50))
        odd = not odd
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
                    blocks.pop(idx+1)
                    blocks.pop(idx)
                elif direction == 1 and (x+50,y) in blocks:
                    idx = blocks.index((x+50,y))
                    blocks.pop(idx+1)
                    blocks.pop(idx)
                elif direction == 2 and (x,y-50) in blocks:
                    idx = blocks.index((x,y-50))
                    blocks.pop(idx+1)
                    blocks.pop(idx)
                elif direction == 3 and (x,y+50) in blocks:
                    idx = blocks.index((x,y+50))
                    blocks.pop(idx+1)
                    blocks.pop(idx)
            if event.key == pygame.K_z:
                if direction == 0 and (x - 50, y) not in blocks:      #where the player can place blocks
                    blocks.append((x - 50, y))
                    blocks.append(typeponter)
                elif direction == 1 and (x + 50, y) not in blocks:
                    blocks.append((x + 50, y))
                    blocks.append(typeponter)
                elif direction == 2 and (x, y - 50) not in blocks:
                    blocks.append((x, y - 50))
                    blocks.append(typeponter)
                elif direction == 3 and (x, y + 50) not in blocks:
                    blocks.append((x, y + 50))
                    blocks.append(typeponter)
            if event.key == pygame.K_SPACE:
                typeponter = (typeponter + 1) % lenoftypes
    if hp <= 0:
        died=True
        running=False
    pygame.display.update()
    pygame.time.Clock().tick(30)
print("Thanks for playing!")
if died:
    hp=10
    win.fill((0, 0, 0))
    text = text_font.render("You died!", True, (255, 0, 0))
    win.blit(text, (200, 200))
    pygame.display.update()
    pygame.time.wait(2000)
with open('blocks.json', 'w') as f:
    data = {
        "b": blocks,
        'X':x,
        'Y':y,
        'HP':hp,
        'd':direction
    }
    json.dump(data, f)
pygame.quit()
