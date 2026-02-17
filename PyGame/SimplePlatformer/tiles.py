import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, image):
        super().__init__()
        self.rect = rect
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))