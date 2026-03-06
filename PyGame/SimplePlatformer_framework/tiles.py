import pygame, os

class Wall(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(os.path.dirname(__file__)+"\\assets\\empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class Water(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(os.path.dirname(__file__)+"\\assets\\empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class Ladder(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(os.path.dirname(__file__)+"\\assets\\empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class Platform(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(os.path.dirname(__file__)+"\\assets\\empty.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))