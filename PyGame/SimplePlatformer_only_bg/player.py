import pygame, os
from pygame import Vector2 as Vec
from settings import UP_KEYS, DOWN_KEYS, LEFT_KEYS, RIGHT_KEYS, PLAYER_SPEED, PLAYER_LIFE, JUMP_STRENGTH

class Player(pygame.sprite.Sprite):
    def __init__(self, rect:pygame.Rect, colour:tuple):
        super().__init__()
        