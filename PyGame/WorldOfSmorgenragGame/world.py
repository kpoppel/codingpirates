import pygame
from settings import TILE_SIZE, WIDTH, GRAVITY, DT, DRAG, WATER_DRAG, SCALE, PLAYER_LIFE
from tiles import *
from entities import *
from player import Player
from game import Game
from level import Level

class World:
    def __init__(self, screen:pygame.Surface, level:Level, org_screen:pygame.Surface):
        self.screen = screen
        self.org_screen = org_screen
        self.level = level
        self.gravity = GRAVITY
        self.game = Game(self.screen)
        self._setupWorld()
        self.previous_life = PLAYER_LIFE
        

    def _setupWorld(self):
        # print("New player made")
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(pygame.Rect(self.level.spawn_x, self.level.spawn_y, TILE_SIZE/2, TILE_SIZE/2), (255,0,0)))

    def _applyGravity(self, player):
        if player.in_water:
            player.vel.y += self.gravity/2
            player.vel.y *= WATER_DRAG
        else:
            if not player.on_ladder:
                player.vel.y += self.gravity
            else:
                player.vel.y *= DRAG
        player.rect.y += player.vel.y * DT

    def _horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.vel.x * DT
        if player.in_water:
            player.vel.x *= WATER_DRAG
        else:
            player.vel.x *= DRAG
        for sprite in self.level.walls.sprites():
            if sprite.rect.colliderect(player.rect):
                # checks if moving towards left
                if player.vel.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    player.vel.x = 0
                # checks if moving towards right
                elif player.vel.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    player.vel.x = 0
        if player.on_left and player.vel.x >= 0:
            player.on_left = False
        if player.on_right and player.vel.x <= 0:
            player.on_right = False

    def _vertical_movement_collision(self):
        player = self.player.sprite
        self._applyGravity(player)
        for sprite in self.level.walls.sprites():
            if sprite.rect.colliderect(player.rect):
                # checks if moving towards bottom, except when holding down and on platform
                if player.vel.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.vel.y = 0
                    player.on_ground = True
                # checks if moving towards up
                elif player.vel.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.vel.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.vel.y < 0 or player.vel.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.vel.y > 0:
            player.on_ceiling = False

    def _water_collision(self):
        player = self.player.sprite
        player.in_water = False
        for sprite in self.level.water.sprites():
            if sprite.rect.colliderect(player.rect):
                player.in_water = True
                break

    def _lava_collision(self):
        player = self.player.sprite
        player.in_lava = False
        player.in_water = False
        for sprite in self.level.lava.sprites():
            if sprite.rect.colliderect(player.rect):
                player.in_lava = True
                player.in_water = True
                break

        if player.in_lava:
            if player.lava_tick >= 60:
                player.life -= 1
                player.lava_tick = 0

    def _ladder_collision(self):
        player = self.player.sprite
        player.on_ladder = False
        for sprite in self.level.ladders.sprites():
            if sprite.rect.colliderect(player.rect):
                player.on_ladder = True

    def _platform_collision(self):
        player = self.player.sprite
        player.on_platform = False
        for sprite in self.level.platforms.sprites():
            if sprite.rect.colliderect(player.rect):
                player.on_platform = True
                if player.vel.y > 0:
                    if player.on_platform and not player.down:
                        player.rect.bottom = sprite.rect.top
                        player.vel.y = 0
                        player.on_ground = True
                    else:
                        player.on_platform = False
    
    def _door_collision(self):
        player = self.player.sprite
        for sprite in self.level.doors.sprites():
            if sprite.rect.colliderect(player.rect):
                # checks if moving towards left
                if player.vel.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    player.vel.x = 0
                # checks if moving towards right
                elif player.vel.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    player.vel.x = 0

        for sprite in self.level.doors.sprites():
            if sprite.rect.colliderect(player.rect):
                # checks if moving towards bottom, except when holding down and on platform
                if player.vel.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.vel.y = 0
                    player.on_ground = True
                # checks if moving towards up
                elif player.vel.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.vel.y = 0
                    player.on_ceiling = True
    
    def _handle_coins(self):
        player = self.player.sprite
        for coin in self.level.coins.sprites():
            if coin.rect.colliderect(player.rect):
                player.coins += 1
                self.level.coins.remove(coin)

    def _handle_keys(self):
        player = self.player.sprite
        for key in self.level.keys.sprites():
            if key.rect.colliderect(player.rect):
                player.inv.append(key.colour+"_key")
                self.level.keys.remove(key)
                print(player.inv)

    def _handle_enemies(self):
        player = self.player.sprite
        for enemy in self.level.SpikedCubes.sprites():
            if enemy.rect.colliderect(player.rect) and player.lava_tick >= 60:
                player.life -= 1
                player.lava_tick = 0
            enemy.move()

    def _open_doors(self):
        player = self.player.sprite
        for door in self.level.doors.sprites():
            if player.rect.colliderect(door):
                door.openDoor(player)
            if door.open:
                self.level.doors.remove(door)

    def _handle_FinishFlag(self):
        player = self.player.sprite
        for FinishFlag in self.level.FinishFlag.sprites():
            if player.rect.colliderect(FinishFlag):
                player.game_won = True

    def update_level(self, level:Level, dir):
        self.level = level
        player_pos = self.player.sprite.rect
        if dir == "w":
            player_pos.x = self.level.width - 1
            player_pos.y -= 8
        elif dir == "e":
            player_pos.x = -player_pos.width + 1
            player_pos.y -= 8
        elif dir == "n":
            player_pos.y = self.level.height - 1
        elif dir == "s":
            player_pos.y = -player_pos.height + 1
        elif dir == "r":
            player_pos.x = self.level.width // 2
            player_pos.y = self.level.height // 2
        elif dir == "reset":
            player_pos.x = self.level.spawn_x
            player_pos.y = self.level.spawn_y
            self._setupWorld()

    def update(self, keys, last_key, events):
        self.level.coins.draw(self.screen)
        self.level.chests.draw(self.screen)
        self.level.keys.draw(self.screen)
        self.level.doors.draw(self.screen)
        self.level.SpikedCubes.draw(self.screen)
        self.level.FinishFlag.draw(self.screen)

        # Movement and collision
        self._ladder_collision()
        self._horizontal_movement_collision()
        self._vertical_movement_collision()
        self._open_doors()
        self._door_collision()
        self._platform_collision()
        self._lava_collision()
        if not self.player.sprite.in_lava:
            self._water_collision()

        # Handle entity interactions
        self._handle_coins()
        self._handle_keys()
        self._handle_enemies()
        self._handle_FinishFlag()

        # Update player
        self.player.update(keys, last_key, events)
        self.player.draw(self.screen)

        if self.player.sprite.life < self.previous_life:
            self.player.sprite.display_damage = True
        self.previous_life = self.player.sprite.life

        # Updates game
        self.game.game_state(self.player.sprite, self.org_screen)
