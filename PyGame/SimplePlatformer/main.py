import pygame, os, sys
from world import World
from settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("[GAME NAME HERE]")

class Platformer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.level = 1

    def getMap(self):
        filepath = os.path.dirname(__file__)+"\\levels\\lvl"+str(self.level)+"\\bg.png"
        self.bg = pygame.image.load(filepath)
        self.bg = pygame.transform.scale(self.bg, (WIDTH,HEIGHT))

    def getMapData(self):
        filepath = os.path.dirname(__file__)+"\\levels\\lvl"+str(self.level)+"\\mapData.csv"
        self.map_data = filepath
        filepath = os.path.dirname(__file__)+"\\levels\\lvl"+str(self.level)+"\\data.json"
        self.map_json = open(filepath, "r")

    def main(self):
        self.getMapData()
        world = World(self.map_data, self.map_json, self.screen)
        self.getMap()
        while True:
            self.screen.blit(self.bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.pressed_keys = pygame.key.get_pressed()
            # print(self.pressed_keys)
            world.update(self.pressed_keys)
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    play = Platformer(screen, WIDTH, HEIGHT)
    play.main()