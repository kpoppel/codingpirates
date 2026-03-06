import pygame
from settings import WIDTH, HEIGHT

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 36)
        self.message_color = pygame.Color("red")

    # Function to lose the game
    def _game_lose(self, player):
        player.game_over = True
        message = self.font.render('You Lose...', True, self.message_color)
        self.screen.blit(message,(WIDTH // 3 + 70, 70))

    # Function to win the game
    def _game_win(self, player):
        player.game_over = True
        player.win = True
        message = self.font.render('You Win!!', True, self.message_color)
        self.screen.blit(message,(WIDTH // 3, 70))

    # Function to render the text for keeping track of player coins
    def _draw_coins(self, player):
        message = self.font.render("Coins: "+str(player.coins), True, pygame.Color("darkorange"))
        self.screen.blit(message, (30,30))

    # Function called every frame to update game state
    def game_state(self, player):
        if player.life <= 0 or player.rect.y >= HEIGHT:
            self._game_lose(player)
        self._draw_coins(player)