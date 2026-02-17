import pygame
from settings import WIDTH, HEIGHT

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 70)
        self.message_color = pygame.Color("black")

    def _game_lose(self, player):
        player.game_over = True
        message = self.font.render('You Lose...', True, self.message_color)
        self.screen.blit(message,(WIDTH // 3 + 70, 70))

    def _game_win(self, player):
        player.game_over = True
        player.win = True
        message = self.font.render('You Win!!', True, self.message_color)
        self.screen.blit(message,(WIDTH // 3, 70))

    def game_state(self, player):
        if player.life <= 0 or player.rect.y >= HEIGHT:
            self._game_lose(player)