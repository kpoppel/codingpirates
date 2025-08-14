# Vi skifter display til TFT 160x128 farvedisplay
# Gem filen som "main.py" på ESP32
import _thread
from HAL import HAL
from Sprite import Sprite
import time

class Game:
    def __init__(self, hal):
        self.hal = hal
        self.player_1 = Sprite(hal.framebuffer, hal.SCREEN_WIDTH, hal.SCREEN_HEIGHT, "sprites.json", "player_1", True)
        self.player_2 = Sprite(hal.framebuffer, hal.SCREEN_WIDTH, hal.SCREEN_HEIGHT, "sprites.json", "player_2", True)
        self.reset()
        
    def reset(self):
        self.player_1.goto(56,8)
        self.player_2.goto(60,12)

    def control(self):
        # Koden skal udvides til at bruge de 8 3D-printede knapper
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
            self.player_1.move_up()

        if not self.hal.button[1]():
            print("Button_2")
            self.player_1.move_down()

        if not self.hal.button[2]():
            print("Button_3")
            self.player_1.move_left()

        if not self.hal.button[3]():
            print("Button_4")
            self.player_1.move_right()

        if not self.hal.button[4]():
            print("Button_5")
            self.player_2.move_up()

        if not self.hal.button[5]():
            print("Button_6")
            self.player_2.move_down()

        if not self.hal.button[6]():
            print("Button_7")
            self.player_2.move_left()
            #self.player_2.move_right()
            self.player_2.move_down()

        if not self.hal.button[7]():
            print("Button_8")
            self.player_2.move_right()

    def loop(self):
        while True:
            self.hal.framebuffer.fill(0)
            
            self.player_1.draw()
            self.player_2.draw()
            
            # Collision check
            if self.player_2.collided == True or self.player_1.was_off_screen:
                print("Spillet er tabt!")
                time.sleep(2)
                self.reset()
                
            self.hal.show()
            self.control()
            #time.sleep(1)

    def run(self):
        # Start screen update thread
        _thread.start_new_thread(self.loop, ())

###
hal = HAL()
game = Game(hal)
game.run()

