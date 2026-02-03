import pygame
import json
# from file_path import get_path
from math import floor
from random import randint

# pygame setup
pygame.init()

scale = 3
gridSize = 8*scale

dt = 1/60

screen = pygame.display.set_mode((296*scale, 304*scale))
clock = pygame.time.Clock()

background = pygame.image.load("PyGame/SimplePlatformer/levels/lvl1/_composite.png")
background = pygame.transform.scale(background, (296*scale,304*scale))

def parseCSV(file):
    f = open(file, "r")

    contentArray = []
    tileArray = []
    x = 0
    y = 0

    EOFReached = False
    while EOFReached == False:
        line = f.readline()
        if line == "":
            EOFReached = True
            break
        linecontents = [cell.strip() for cell in line.split(",") if cell.strip()]
        
        for tile in linecontents:
            tile = tile.strip()
            if tile == "1":
                tileArray.append(pygame.Rect(x*8*scale, y*8*scale, gridSize, gridSize))
                # print(f"Tile at grid ({x}, {y}) -> pixel ({x*8*scale}, {y*8*scale})")
            x += 1

        contentArray.append(linecontents)
        y += 1
        x = 0
    return contentArray, tileArray

level1Data, level1Tiles = parseCSV("PyGame/SimplePlatformer/levels/lvl1/IntGrid_layer.csv")
level1JSON = json.load(open("PyGame/SimplePlatformer/levels/lvl1/data.json"))

for tile in level1Tiles:
    print(tile.topleft, tile.bottomright)

player = {
    "pos": pygame.Vector2(0,0),
    "vel": pygame.Vector2(0,0),
    "w": gridSize/2,
    "rect": pygame.Rect(0,0,gridSize/2,gridSize/2)
}

player["pos"].x = level1JSON["entities"]["PlayerSpawn"][0]["x"]*scale
player["pos"].y = level1JSON["entities"]["PlayerSpawn"][0]["y"]*scale

def collideWall():
    # Check collisions on X axis
    player["rect"] = pygame.Rect(player["pos"].x, player["pos"].y, gridSize/2, gridSize/2)
    for tile in level1Tiles:
        if player["rect"].colliderect(tile):
            if player["vel"].x > 0:  # Moving right
                player["pos"].x = tile.left - gridSize/2
            elif player["vel"].x < 0:  # Moving left
                player["pos"].x = tile.right
            player["vel"].x = 0
    
    # Check collisions on Y axis
    player["rect"] = pygame.Rect(player["pos"].x, player["pos"].y, gridSize/2, gridSize/2)
    for tile in level1Tiles:
        if player["rect"].colliderect(tile):
            if player["vel"].y > 0:  # Moving down
                player["pos"].y = tile.top - gridSize/2
            elif player["vel"].y < 0:  # Moving up
                player["pos"].y = tile.bottom
            player["vel"].y = 0
running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player["vel"].y -= 50 * dt
    if keys[pygame.K_s]:
        player["vel"].y += 50 * dt
    if keys[pygame.K_a]:
        player["vel"].x -= 50 * dt
    if keys[pygame.K_d]:
        player["vel"].x += 50 * dt
    
    player["pos"] += player["vel"]

    player["vel"].y += 20 * dt
    player["vel"] *= 0.9

    collideWall()

    screen.blit(background, (0,0))
    i = 0
    for tile in level1Tiles:
        temp = i*10
        colour = pygame.Color(0,255,0)
        if i>25:
            i = 0
        colour.g = int(i*10)
        offsetTile = tile.move(0, 0)
        pygame.draw.rect(screen, colour, offsetTile)
        i += 1

    pygame.draw.rect(screen, "red", player["rect"])

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    if (clock.get_fps() == 0):
        dt = 1/60
    else:
        dt = 1/clock.get_fps()

pygame.quit()