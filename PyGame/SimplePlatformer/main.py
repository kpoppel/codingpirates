import pygame, sys
from world import World
from settings import *
import level

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("[GAME NAME HERE]")

class Platformer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.last_key = False
        self.level = 1
        self._load_levels()

    # Function to load all levels
    def _load_levels(self):
        self.levels = {}
        if INFO.levelStartsFromOne:
            for i in range(1,INFO.levelAmount+1):
                self.levels[i] = level.Level(self.width, self.height, i)
        else:
            for i in range(0, INFO.levelAmount+1):
                self.levels[i] = level.Level(self.width, self.height, i)

    def switchLevel(self, world):
        self.level += 1
        if self.level > self.levels.__len__():
            self.level = 1
        world.update_level(self.levels[self.level])
    
    # Main game loop, runs every frame
    def main(self):
        world = World(self.screen, self.levels[self.level])
        while True:
            self.screen.blit(self.levels[self.level].bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_0:
                        self.switchLevel(world)
                if event.type == pygame.KEYUP:
                    self.last_key = event.dict["key"]
                    
            self.pressed_keys = pygame.key.get_pressed()

            world.update(self.pressed_keys, self.last_key)
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    play = Platformer(screen, WIDTH, HEIGHT)
    play.main()