import pygame, os
from settings import INFO

class Wall(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class Water(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class Ladder(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class Platform(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class Lava(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(INFO.assetsPath+"empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))