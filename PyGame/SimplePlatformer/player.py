import pygame, os
from pygame import Vector2 as Vec
from settings import UP_KEYS, DOWN_KEYS, LEFT_KEYS, RIGHT_KEYS, PLAYER_SPEED, PLAYER_LIFE, JUMP_STRENGTH

class Player(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, colour:tuple):
        super().__init__()
        self.rect = rect
        self.image = pygame.image.load(os.path.dirname(__file__)+"\\assets\\red.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.colour = colour
        self.vel = Vec(0,0)
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.life = PLAYER_LIFE

    def _get_keys_in_list(self, keys, list):
        for key in list:
            if keys[key]:
                return True

    def update(self, keys):
        if self._get_keys_in_list(keys, UP_KEYS):
            if self.on_ground:
                self.vel.y = -JUMP_STRENGTH
        if self._get_keys_in_list(keys, DOWN_KEYS):
            pass
        if self._get_keys_in_list(keys, LEFT_KEYS):
            self.vel.x -= PLAYER_SPEED
        if self._get_keys_in_list(keys, RIGHT_KEYS):
            self.vel.x += PLAYER_SPEED