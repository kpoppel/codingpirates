# Register entities in this file, coin below as simple example
import pygame
from settings import INFO

class Coin(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"coin.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))