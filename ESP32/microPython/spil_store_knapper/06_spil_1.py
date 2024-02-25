# Første forsøg på et spil med knapper og det lille display
import _thread
import HAL
from Sprite import Sprite

class Game:
    def __init__(self, hal):
        self.hal = hal
        self.player_1 = Sprite(hal.display, "sprites.json", "player_1")
        self.player_2 = Sprite(hal.display, "sprites.json", "player_2")
        self.reset()
        
    def reset(self):
        self.player_1.goto(56,8)
        self.player_2.goto(60,12)

    def control(self):
        if not self.hal.button_board[0]():
            print("Button_1")
            # Hold Spriten på skærmen
            if not self.player_1.off_screen():
                self.player_1.move_up()
                #self.player_1.move_down()
                #self.player_1.move_left()
                #self.player_1.move_right()

        if not self.hal.button_board[1]():
            print("Button_2")
            if not self.player_2.off_screen():
                self.player_2.move_up()
                #self.player_2.move_down()
                #self.player_2.move_left()
                #self.player_2.move_right()

    def loop(self):
        while True:
            self.hal.display.fill(0)
            
            self.player_1.draw()
            self.player_2.draw()
            
            # Collision check
            if self.player_2.collided == True:
                print("Spillet er tabt!")
                time.sleep(2)
                self.reset()
                
            self.hal.display.show()
            self.control()

    def run(self):
        # Start screen update thread
        _thread.start_new_thread(self.loop, ())

###
hal = HAL.HAL()
game = Game(hal)
game.loop()