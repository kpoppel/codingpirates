import HAL
from Sprite import Sprite

class Game:
    def __init__(self, hal):
        self.hal = hal
        self.player_1 = Sprite(hal.display, "sprites.json", "player_1")
        self.player_2 = Sprite(hal.display, "sprites.json", "player_2")
        self.player_1.goto(56,8)
        self.player_2.goto(60,12)

    def loop(self):
        while True:
            self.hal.display.fill(0)
            
            self.player_1.draw()
            self.player_2.draw()
            
            self.hal.display.show()


hal = HAL.HAL()
game = Game(hal)
game.loop()