import pygame, sys
from world import World
from settings import *
from level import Level

pygame.init()

org_screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = org_screen.copy()
pygame.display.set_caption("[GAME NAME HERE]")

class Platformer:
    def __init__(self, screen, width, height, org_screen):
        self.screen = screen
        self.org_screen = org_screen
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.last_key = False
        self.level = ""
        self.start_level = ""
        self._load_levels()

    # Function to load all levels
    def _load_levels(self):
        self.levels = {}
        if INFO.levelStartsFromOne:
            for i in range(1,INFO.levelAmount+1):
                level = Level(self.width, self.height, i)
                self.levels[level.iid] = level
        else:
            for i in range(0, INFO.levelAmount):
                level = Level(self.width, self.height, i)
                self.levels[level.iid] = level
        
        for level in self.levels.values():
            if level.player_spawn != (0,0):
                self.level = level.iid
                self.start_level = level.iid
                break

    def switchLevel(self, world, player, reset=False):
        if reset:
            self.level = self.start_level
            world.update_level(self.levels[self.level], "reset")
        if player.rect.x < -player.rect.width:
            if "w" in self.levels[self.level].neighbours:
                self.level = self.levels[self.level].neighbours["w"]
                world.update_level(self.levels[self.level], "w")
        if player.rect.x > self.width:
            if "e" in self.levels[self.level].neighbours:
                self.level = self.levels[self.level].neighbours["e"]
                world.update_level(self.levels[self.level], "e")
        if player.rect.y < -player.rect.height:
            if "n" in self.levels[self.level].neighbours:
                self.level = self.levels[self.level].neighbours["n"]
                world.update_level(self.levels[self.level], "n")
        if player.rect.y > self.height:
            if "s" in self.levels[self.level].neighbours:
                self.level = self.levels[self.level].neighbours["s"]
                world.update_level(self.levels[self.level], "s")
        if player.rect.y > self.height + player.rect.height:
            world.update_level(self.levels[self.level], "r")
            

    # Main game loop, runs every frame
    def main(self):
        world = World(self.screen, self.levels[self.level], self.org_screen)
        while True:
            self.screen.blit(self.levels[self.level].bg, (0, 0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    self.last_key = event.dict["key"]
                if event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_r:
                        self._load_levels()
                        self.switchLevel(world, world.player.sprite, reset=True)
                        
                    
            self.pressed_keys = pygame.key.get_pressed()

            if not world.player.sprite.game_over:
                self.switchLevel(world, world.player.sprite)
                world.update(self.pressed_keys, self.last_key, events)
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    play = Platformer(screen, WIDTH, HEIGHT, org_screen)
    play.main()