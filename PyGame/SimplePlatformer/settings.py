import pygame, types, os
BASE_WIDTH = 256 # Base image width
BASE_HEIGHT = 256 # Base image height
BASE_TILE_SIZE = 8 # Tile size on base image
SCALE = 3 # Scaling factor from base image

WIDTH = BASE_WIDTH * SCALE # Actual width
HEIGHT = BASE_HEIGHT * SCALE # Actual height
TILE_SIZE = 8 * SCALE # Actual tile size of grid

GRAVITY = 50 # Downwards acceleration in [px/s^2]
DRAG = 0.90 # Retention of energy per frame
JUMP_STRENGTH = 1000 # Immediate acceleration to JUMP_STRENGTH [px/s]
WATER_DRAG = 0.8 # Retention of energy per frame in water
LAVA_DAMAGE = 1 # Lava damage per second

UP_KEYS = [pygame.K_SPACE, pygame.K_w, pygame.K_UP] # Keys for upwards movement
DOWN_KEYS = [pygame.K_s, pygame.K_LCTRL, pygame.K_DOWN] # Keys for downwards movement
LEFT_KEYS = [pygame.K_a, pygame.K_LEFT] # Keys for leftwards movement
RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT] # Keys for rightwards movement
PLAYER_SPEED = 30 # Player acceleration in [px/s^2]
PLAYER_LIFE = 5 # Player starting health
PLAYER_MAX_LIFE = 5 # Player max health

DT = 1/60 # Delta time, time between each frame

# INFO stores various base locations to help with file systems
INFO = types.SimpleNamespace(
    levelAmount = 8,
    assetsPath = os.path.join(os.path.dirname(__file__), "assets", ""),
    levelsPath = os.path.join(os.path.dirname(__file__), "levels", ""),
    levelFileNames = types.SimpleNamespace(
        background = "_composite.png",
        jsonData = "data.json",
        csvData = "Walls.csv"
    ),
    levelStartsFromOne = True
)

TICKS = types.SimpleNamespace(
    lavaTick = 60,
    jumpTick = 8,
    damageDisplayTick = 10
)

ASSETS = types.SimpleNamespace(
    heart = pygame.transform.scale(pygame.image.load(INFO.assetsPath + "heart.png"), (45,45)),
    damage = pygame.transform.scale(pygame.image.load(INFO.assetsPath + "red.png"), (WIDTH, HEIGHT))
)