import pygame, os
from tiles import *
from entities import *
from settings import *
import json

class Level:
    def __init__(self, width, height, level):
        self.width = width
        self.height = height
        self.level = level
        self._getMap()
        self._getMapData()
        self._setUpLevel()

    def _getMap(self):
        filepath = os.path.dirname(__file__)+"\\levels\\lvl"+str(self.level)+"\\bg.png"
        self.bg = pygame.image.load(filepath)
        self.bg = pygame.transform.scale(self.bg, (self.width,self.height))

    def _getMapData(self):
        filepath = os.path.dirname(__file__)+"\\levels\\lvl"+str(self.level)+"\\mapData.csv"
        self.map_data = filepath
        filepath = os.path.dirname(__file__)+"\\levels\\lvl"+str(self.level)+"\\data.json"
        self.map_json = open(filepath, "r")
        self.dat = json.load(self.map_json)

    def _setUpLevel(self):
        # World tiles
        self.walls = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()

        parsedWalls = self._parseCSV("1")
        for tile in parsedWalls:
            wall = Wall(pygame.Rect(tile[0]*TILE_SIZE, tile[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            self.walls.add(wall)

        parsedWater = self._parseCSV("2")
        for tile in parsedWater:
            water = Water(pygame.Rect(tile[0]*TILE_SIZE, tile[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            self.water.add(water)

        parsedLadders = self._parseCSV("3")
        for tile in parsedLadders:
            ladder = Ladder(pygame.Rect(tile[0]*TILE_SIZE, tile[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            self.ladders.add(ladder)

        parsedPlatforms = self._parseCSV("4")
        for tile in parsedPlatforms:
            platform = Platform(pygame.Rect(tile[0]*TILE_SIZE, tile[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            self.platforms.add(platform)

        # World entities
        self.coins = pygame.sprite.Group()
        if "Coin" in self.dat["entities"].keys():
            for entity in self.dat["entities"]["Coin"]:
                coin = Coin(pygame.Rect(entity["x"] * SCALE, entity["y"] * SCALE, entity["width"] * SCALE, entity["height"] * SCALE))
                self.coins.add(coin)

        # Player spawn
        if "PlayerSpawn" in self.dat["entities"].keys():
            self.player_spawn = (self.dat["entities"]["PlayerSpawn"][0]["x"], self.dat["entities"]["PlayerSpawn"][0]["y"])
        else:
            self.player_spawn = (0, 0)

        self.spawn_x = int(self.player_spawn[0] * SCALE)
        self.spawn_y = int(self.player_spawn[1] * SCALE)

    def _parseCSV(self, key:str):
        f = open(self.map_data, "r")

        contentArray = []
        x = 0
        y = 0

        for line in f:
            linecontents = [cell.strip() for cell in line.split(",")]
            for tile in linecontents:
                tile = tile.strip()
                if tile == key:
                    contentArray.append((x,y))
                x += 1
            y += 1
            x = 0
        return contentArray