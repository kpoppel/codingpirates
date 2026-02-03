import pygame
from pygame import Vector2 as Vec
from settings import UP_KEYS, DOWN_KEYS, LEFT_KEYS, RIGHT_KEYS, PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    vel = Vec(0,0)
    
    def __init__(self, rect:pygame.Rect, colour:tuple):
        super().__init__()
        self.rect = rect
        self.colour = colour
    
    def update(self, event):
        if event in UP_KEYS:
            if self.on_ground:
                self.vel.y = -PLAYER_SPEED*10
        elif event in DOWN_KEYS:
            pass
        elif event in LEFT_KEYS:
            self.vel.x -= PLAYER_SPEED
        elif event in RIGHT_KEYS:
            self.vel.x += PLAYER_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)