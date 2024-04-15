# Første forsøg på et spil med knapper og det lille display
import _thread
from HAL import HAL
from Sprite import Sprite
import time

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
        # Koden skal udvides til at bruge de 8 3D-printede knapper
        # Og så skjuler der sig en udfordring nå spriten går off_screen...
        if not self.hal.button_board[0]():
            print("Board Button_1")
            # Hold Spriten på skærmen
            if not self.player_1.off_screen():
                self.player_1.move_up()
                #self.player_1.move_down()
                #self.player_1.move_left()
                #self.player_1.move_right()

        if not self.hal.button_board[1]():
            print("Board Button_2")
            if not self.player_2.off_screen():
                self.player_2.move_up()
                #self.player_2.move_down()
                #self.player_2.move_left()
                #self.player_2.move_right()

        if not self.hal.button[0]():
            print("Button_1")
            # Hold Spriten på skærmen
            self.player_1.move_up()
            if not self.player_1.off_screen():
                self.player_1.move_down()

        if not self.hal.button[1]():
            print("Button_2")
            # Hold Spriten på skærmen
            self.player_1.move_down()
            if not self.player_1.off_screen():
                self.player_1.move_up()

        if not self.hal.button[2]():
            print("Button_3")
            # Hold Spriten på skærmen
            self.player_1.move_left()
            if not self.player_1.off_screen():
                self.player_1.move_right()

        if not self.hal.button[3]():
            print("Button_4")
            # Hold Spriten på skærmen
            self.player_1.move_right()
            if not self.player_1.off_screen():
                self.player_1.move_left()

        if not self.hal.button[4]():
            print("Button_5")
            # Hold Spriten på skærmen
            self.player_2.move_up()
            if not self.player_2.off_screen():
                self.player_2.move_down()

        if not self.hal.button[5]():
            print("Button_6")
            # Hold Spriten på skærmen
            self.player_2.move_down()
            if not self.player_2.off_screen():
                self.player_2.move_up()

        if not self.hal.button[6]():
            print("Button_7")
            # Hold Spriten på skærmen
            self.player_2.move_left()
            if not self.player_2.off_screen():
                self.player_2.move_right()

        if not self.hal.button[7]():
            print("Button_8")
            # Hold Spriten på skærmen
            self.player_2.move_right()
            if not self.player_2.off_screen():
                self.player_2.move_left()




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
hal = HAL()
game = Game(hal)
game.run()