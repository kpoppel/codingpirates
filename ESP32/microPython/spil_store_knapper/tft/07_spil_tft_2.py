# Første forsøg på et spil med knapper og det lille display
import _thread
from HAL import HAL
from Sprite import SpriteController, SpriteImage
import time
import random

class Game:
    def __init__(self, hal):
        self.hal = hal
        # Vi kan indlæse json sort/hvis sprites:
        #sprite = SpriteImage("sprites.json")
        #sprite.load_json("player_1")
        # Eller de nye farvesprites:
        sprite = SpriteImage("ball.rgb")
        sprite.load_rgb565()
        self.player_1 = SpriteController(sprite, hal.framebuffer, hal.SCREEN_WIDTH, hal.SCREEN_HEIGHT, True)
        # json sprite:
        #sprite = SpriteImage("sprites.json")
        #sprite.load_json("player_2")
        sprite = SpriteImage("ball_2.rgb")
        sprite.load_rgb565()
        self.player_2 = SpriteController(sprite, hal.framebuffer, hal.SCREEN_WIDTH, hal.SCREEN_HEIGHT, True)
        self.reset()
        
    def reset(self):
        self.player_1.goto(56,64)
        self.player_2.goto(60,32)

    def control(self):
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
            #print("Button_7")
            self.player_2.move_left()
            #self.player_2.move_right()
            self.player_2.move_down()

        if not self.hal.button[7]():
            #print("Button_8")
            self.player_2.move_right()

    def control_2(self):
        # Make player 1 fumble around using the Sprite features
        if self.player_1.was_off_screen:
            self.player_1.direction(random.randint(0, 359))
            self.player_1.speed(random.randint(1, 6))
        self.player_1.move()

        # Make player 2 fumble around using the Sprite features
        if self.player_2.was_off_screen:
            self.player_2.direction(random.randint(0, 359))
            self.player_2.speed(random.randint(1, 6))
        self.player_2.move()
        

    def loop(self):
        count = 0
        #  0 : up
        #  90: left
        # 180: down
        # 270: right
        self.player_1.direction(random.randint(0,359))
        self.player_1.speed(2)
        self.player_2.direction(random.randint(0,359))
        self.player_2.speed(2)
        while True:
        #if 1:
            self.hal.framebuffer.text(f'{count} {self.player_2.x} {self.player_2.y}', 0, 0, 0x7512)
            count += 1
            
            self.player_1.draw()
            self.player_2.draw()
            
            # Collision check
            #if self.player_2.collided == True or self.player_1.was_off_screen:
            #    print("Spillet er tabt!")
                #time.sleep(2)
            #    self.reset()
                
            self.control_2()
            self.hal.show()
            self.hal.framebuffer.fill(0)
            #time.sleep_ms(100)

    def run(self):
        # Start screen update thread
        _thread.start_new_thread(self.loop, ())

###
hal = HAL()
game = Game(hal)
game.run()
#for x in range(1000):
#    game.loop()