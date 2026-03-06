# Register entities in this file, coin below as simple example
import pygame, os

class Coin(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(os.path.dirname(__file__)+"\\assets\\coin.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))