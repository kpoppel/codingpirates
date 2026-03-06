import pygame, os, json
from settings import TILE_SIZE, WIDTH, GRAVITY, DT, DRAG, WATER_DRAG, SCALE
from tiles import *
from player import Player
from game import Game

class World:
    def __init__(self, map_data, map_json, screen):
        self.screen = screen
        self.map_data = map_data
        self.dat = json.load(map_json)
        self._setupWorld(map_json)
        self.gravity = GRAVITY
        self.game = Game(self.screen)
        

    def _setupWorld(self, map_json):
        # World tiles
        self.walls = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()

        parsedWalls = self._parseCSV("1")
        for tile in parsedWalls:
            wall = Wall(pygame.Rect(tile[0]*TILE_SIZE, tile[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            self.walls.add(wall)

        # Player and spawn
        self.player = pygame.sprite.GroupSingle()
        self.player_spawn = (self.dat["entities"]["PlayerSpawn"][0]["x"], self.dat["entities"]["PlayerSpawn"][0]["y"])

        spawn_x = int(self.player_spawn[0] * SCALE)
        spawn_y = int(self.player_spawn[1] * SCALE)

        self.player.add(Player(pygame.Rect(spawn_x, spawn_y, TILE_SIZE/2, TILE_SIZE/2), (255,0,0)))

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

    def _applyGravity(self, player):
        player.vel.y += self.gravity
        player.rect.y += player.vel.y * DT

    def _horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.vel.x * DT
        player.vel.x *= DRAG
        for sprite in self.walls.sprites():
            if sprite.rect.colliderect(player.rect):
                # checks if moving towards left
                if player.vel.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    player.vel.x = 0
                # checks if moving towards right
                elif player.vel.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    player.vel.x = 0
        if player.on_left and player.vel.x >= 0:
            player.on_left = False
        if player.on_right and player.vel.x <= 0:
            player.on_right = False

    def _vertical_movement_collision(self):
        player = self.player.sprite
        self._applyGravity(player)
        for sprite in self.walls.sprites():
            if sprite.rect.colliderect(player.rect):
                # checks if moving towards bottom, except when holding down and on platform
                if player.vel.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.vel.y = 0
                    player.on_ground = True
                # checks if moving towards up
                elif player.vel.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.vel.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.vel.y < 0 or player.vel.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.vel.y > 0:
            player.on_ceiling = False

    def update(self, keys):
        # Movement and collision
        self._horizontal_movement_collision()
        self._vertical_movement_collision()        

        # Update player
        self.player.update(keys)
        self.player.draw(self.screen)

        # Updates game
        self.game.game_state(self.player.sprite)
