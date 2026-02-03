import pygame
import json
from settings import TILE_SIZE, WIDTH, GRAVITY, DT
from tiles import Wall
from player import Player
from game import Game

class World:
    def __init__(self, map_data, map_json, screen):
        self.screen = screen
        self.map_data = map_data
        self._setupWorld(map_json)
        self.gravity = GRAVITY
        self.game = Game(self.screen)

    def _setupWorld(self, map_json):
        self.walls = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.dat = json.load(map_json)
        self.player_spawn = (self.dat["entities"]["PlayerSpawn"][0]["x"], self.dat["entities"]["PlayerSpawn"][0]["y"])

        self.player.add(Player(pygame.Rect(self.player_spawn[0], self.player_spawn[1], TILE_SIZE/2, TILE_SIZE/2), (0,0,0)))

        parsedWalls = self.parseCSV("1")
        for wall in parsedWalls:
            wall2 = Wall(pygame.Rect(wall[0], wall[1], TILE_SIZE, TILE_SIZE))
            self.walls.add(wall2)

    def _applyGravity(self, player):
        player.vel.y += self.gravity
        player.rect.y += player.vel.y * DT

    def _horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.vel.x * DT
        for sprite in self.walls.sprites():
            if sprite.rect.colliderect(player.rect):
                # checks if moving towards left
                if player.vel.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                # checks if moving towards right
                elif player.vel.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
        if player.on_left and player.vel.x >= 0:
            player.on_left = False
        if player.on_right and player.vel.x <= 0:
            player.on_right = False

    def _vertical_movement_collision(self):
        player = self.player.sprite
        self._apply_gravity(player)
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # checks if moving towards bottom
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

    def update(self, events):
        self.walls.update()
        
    def parseCSV(self, key:str):
        contentArray = []
        x = 0
        y = 0

        EOFReached = False
        while EOFReached == False:
            line = self.map_data.readline()
            x = 0
            if line == "":
                EOFReached = True
                break
            linecontents = [cell.strip() for cell in line.split(",") if cell.strip()]

            for tile in linecontents:
                tile = tile.strip()
                if tile == key:
                    contentArray.append((x,y))
                x += 1
            y += 1
            
        return contentArray
    