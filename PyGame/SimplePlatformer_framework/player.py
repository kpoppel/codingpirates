import pygame, os
from pygame import Vector2 as Vec
from settings import UP_KEYS, DOWN_KEYS, LEFT_KEYS, RIGHT_KEYS, PLAYER_SPEED, PLAYER_LIFE, JUMP_STRENGTH, DT

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
        self.in_water = False
        self.on_ladder = False
        self.down = False # Helper for platforms
        self.on_platform = False
        self.coins = 0

    def _get_keys_in_list(self, keys, list):
        for key in list:
            if keys[key]:
                return True

    def update(self, keys):
        if self.on_ladder:
            # Movement on ladders
            if self._get_keys_in_list(keys, UP_KEYS):
                self.vel.y -= PLAYER_SPEED
            if self._get_keys_in_list(keys, DOWN_KEYS):
                self.down = True
                self.vel.y += PLAYER_SPEED
            else:
                self.down = False
            if self._get_keys_in_list(keys, LEFT_KEYS):
                self.vel.x -= PLAYER_SPEED
            if self._get_keys_in_list(keys, RIGHT_KEYS):
                self.vel.x += PLAYER_SPEED

        elif self.in_water:
            # Movement in water
            if self._get_keys_in_list(keys, UP_KEYS):
                self.vel.y = -JUMP_STRENGTH
                self.on_ground = True
            if self._get_keys_in_list(keys, DOWN_KEYS):
                self.vel.y += PLAYER_SPEED/2
                self.down = True
            else:
                self.down = False
            if self._get_keys_in_list(keys, LEFT_KEYS):
                self.vel.x -= PLAYER_SPEED/2
            if self._get_keys_in_list(keys, RIGHT_KEYS):
                self.vel.x += PLAYER_SPEED/2

        else:
            # Movement on land
            if self._get_keys_in_list(keys, UP_KEYS):
                if self.on_ground:
                    self.vel.y = -JUMP_STRENGTH
            if self._get_keys_in_list(keys, DOWN_KEYS):
                self.down = True
            else:
                self.down = False
            if self._get_keys_in_list(keys, LEFT_KEYS):
                self.vel.x -= PLAYER_SPEED
            if self._get_keys_in_list(keys, RIGHT_KEYS):
                self.vel.x += PLAYER_SPEED