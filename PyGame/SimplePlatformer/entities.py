# Register entities in this file, coin below as simple example
import pygame
from settings import INFO

class Coin(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"coin.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

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

    def checkForOpen(self, player):
        if "Gold Key" in player.inv:
            self.open = True
