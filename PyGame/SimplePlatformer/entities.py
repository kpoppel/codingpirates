# Register entities in this file, coin below as simple example
import pygame
from pygame import Vector2 as Vec
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"coin.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))


#---------------------------------------------------Doors
class GoldKey(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"gold_key.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class DoorGoldKey(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"door_gold_key.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.open = False

    def openDoor(self, player):
        if "Gold Key" in player.inv:
            self.open = True
#---------------------------------------------------


#---------------------------------------------------Objects
class Chest(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"chest.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.open = False

    def openChest(self, player):
        if not self.open:
            self.open = True
            player.coins += 1000
#---------------------------------------------------

#---------------------------------------------------Enemies
class SpikedCube(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, data:dict):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"spiked_cube_enemy.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.startPoint = Vec(data["x"]/TILE_SIZE, data["Y"]/TILE_SIZE)
        self.endPoint = Vec(data["customFields"]["EndLocation"]["cx"], data["customFields"]["EndLocation"]["cy"])
        self.speed = data["customFields"]["speed"]
        self.direction = "toEnd"

    def move(self):
        diff = Vec()
        location = Vec(self.rect.x, self.rect.y)
        new_location = Vec()

        if self.direction == "toEnd":
            diff.x = self.endPoint.x - self.rect.x
            diff.y = self.endPoint.y - self.rect.y
        elif self.direction == "toStart":
            diff.x = self.endPoint.x - self.rect.x
            diff.y = self.endPoint.y - self.rect.x
        
        unitVector = diff/diff.length
        movement = unitVector * self.speed

        if self.direction == "toEnd":
            if movement.length > diff.length:
                new_location = self.endPoint
            else:
                new_location = location + movement
                
        elif self.direction == "toStart":
            if movement.length > diff.length:
                new_location = self.startPoint
            else:
                new_location = location + movement
            
        self.rect.x = new_location.x


#---------------------------------------------------