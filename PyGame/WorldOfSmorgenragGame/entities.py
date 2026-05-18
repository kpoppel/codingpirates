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
            player.inv.remove("Gold Key")
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

class Goal(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"goal.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
#---------------------------------------------------

#---------------------------------------------------Enemies
class SpikedCube(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, data:dict):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"spiked_cube_enemy.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.startPoint = Vec(data["x"]*SCALE, data["y"]*SCALE)
        self.endPoint = Vec(data["customFields"]["EndLocation"]["cx"]*TILE_SIZE, data["customFields"]["EndLocation"]["cy"]*TILE_SIZE)
        self.speed = data["customFields"]["Speed"]
        self.direction = "toEnd"
        self.old_unitVector = Vec()

    def move(self):
        diff = Vec()
        location = Vec(self.rect.x, self.rect.y)
        new_location = Vec()

        if self.direction == "toEnd":
            diff = self.endPoint - location
        elif self.direction == "toStart":
            diff = self.startPoint - location
        
        if diff.length() != 0:
            unitVector = diff/diff.length()
        else:
            unitVector = self.old_unitVector * -1
        movement = unitVector * self.speed * DT

        if self.direction == "toEnd":
            if movement.length() > diff.length():
                new_location = self.endPoint
                self.direction = "toStart"
            else:
                new_location = location + movement

        elif self.direction == "toStart":
            if movement.length() > diff.length():
                new_location = self.startPoint
                self.direction = "toEnd"
            else:
                new_location = location + movement
            
        self.rect.x = new_location.x
        self.rect.y = new_location.y
        self.old_unitVector = unitVector.copy()


#---------------------------------------------------