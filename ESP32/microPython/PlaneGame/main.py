import _thread
import ssd1306
import json
import HAL
import time
import random


class Sprites:
    def __init__(self, sprite_file_name):
        try:
            f = open(sprite_file_name)
            self.sprites= json.load(f)
            f.close()
            # Make a list of icon names.
            # Names are in order of insertion from Python 3.7+.
            self.sprite_names = list(self.sprites.keys())
        except:
            self.sprites = None
            self.sprite_names = None
            print("ERROR")
            
    def get(self, name):
        return self.sprites[name]

class Sprite:
    def __init__(self, display, sprite):
        self.display = display
        self.sprite = sprite
        # state:
        self.x = 0
        self.y = 0
        self.collided = False
        self.h = len(self.sprite)
        self.w = len(self.sprite[0])

    def move_up(self, d=1):
        self.y += d
        
    def move_down(self, d=1):
        self.y -= d

    def move_left(self, d=1):
        self.x -= d
        
    def move_right(self, d=1):
        self.x += d
        
    def goto(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def draw(self):
        """ Render the sprite
            Todo: Save some space by rendering to framebuffer on load
        """
        self.collided = False
        for y, row in enumerate(self.sprite):
            for x, data in enumerate(row):
                c = 1 if data=="1" else 0
                if self.display.pixel(x+self.x, y+self.y) == 1:
                    self.collided = True
                self.display.pixel(x+self.x, y+self.y, c)
    
class Landscape:
    def __init__(self, display):
        self.display = display
        # state:
        self.heights = [1 for i in range(128)]

    def scroll(self, speed=1):
        self.heights.pop(0)
        self.heights.append(self.heights[-1]+random.randint(-3,3))
        if self.heights[-1] < 0:
            self.heights[-1] = 0
        if self.heights[-1] > 16:
            self.heights[-1] = 16


    def draw(self):
        for x, h in enumerate(self.heights):
            self.display.line(x, 31, x, 31-h, 1)

class Wall:
    def __init__(self, display):
        self.display = display
        # state:
        self.x = 0
        self.y = 0
        self.h = 12
        self.w = 5
        
    def move_left(self, d=1):
        self.x -= d
        
    def move_right(self, d=1):
        self.x += d
        
    def goto(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def is_visible(self):
        # Is visible if x coordinate
        return (self.x+self.w) > 0
    
    def height(sef, h=16):
        self.h = h
    
    def draw(self):
        #print(f"{self.x},{self.y}")
        self.display.rect(self.x, self.y, self.w, self.h, 1, True)
       
        ### code to move a wall or more and repeat it.
        ### Replaced by Landscape class.
        #for wall in self.walls:
        #    if wall.is_visible():
        #        wall.move_left(self.speed)
        #        wall.draw()
        #    else:
        #        wall.goto(128, 0)
        #        wall.height(32-random.randint(0,16))
        #        if self.speed < 20:
        #            self.speed += 1

        
class Game:
    BACKGROUND_MUSIC_TRACK = 8
    EXPLOSION_TRACK = 7
    GET_READY_TRACK = 9
    def __init__(self, hal, sprites):
        self.hal = hal
        self.player = Sprite(hal.display, sprites.get('player'))
        self.enemy = Sprite(hal.display, sprites.get('enemy'))
        self.shot = Sprite(hal.display, sprites.get('shot'))
        self.landscape = Landscape(hal.display)
        self.reset()
        
    def reset(self):
        #self.walls = list()
        #for wall in range(0,128):
        #    self.walls.append(Wall(hal.display))
        #    self.walls[wall].goto(128+wall, 31)
        self.player.goto(0,0)
        self.enemy.goto(100,8)
        self.shot.goto(90,11)
        # Game stage
        self.speed=1
        self.hal.music.play(self.BACKGROUND_MUSIC_TRACK) # START SCREEN MUSIC?
        self.get_ready_screen()

    def get_ready_screen(self):
        self.hal.display.fill(0)
        self.hal.display.text("GET READY!", int((128-8*10)/2),12, 1)
        self.hal.display.text("(press button)", int((128-8*14)/2),24, 1)
        self.hal.display.show()
        while self.hal.button_1():
            time.sleep_ms(250)
        self.hal.music.play(self.GET_READY_TRACK)
        time.sleep_ms(1000)
        self.hal.display.fill(0)
        self.hal.display.show()
        self.hal.music.play(self.BACKGROUND_MUSIC_TRACK)
 
    def game_over_screen(self):
        self.hal.music.play(self.EXPLOSION_TRACK)
        for i in range(0,4):
            self.hal.display.fill((i+1)%2)
            self.hal.display.text("You are dead!", int((128-8*13)/2),12, i%2)
            self.hal.display.show()
            time.sleep_ms(500)
        self.hal.display.fill(0)
        self.hal.display.show()
        self.reset()

    def game_win_screen(self):
        #self.hal.music.play(9)
        for i in range(0,4):
            self.hal.display.fill((i+1)%2)
            self.hal.display.text("You win!", int((128-8*8)/2),12, i%2)
            self.hal.display.show()
            time.sleep_ms(500)
        self.hal.display.fill(0)
        self.hal.display.show()
        self.reset()
        
    def control(self):
        if not self.hal.button_1():
            #print("Button_1")
            self.player.move_down()
            # How far off screen can we fly? (1 pixel must be visible)
            if self.player.y <= 1 - self.player.h:
                self.player.move_up()
        if not self.hal.button_2():
            #print("Button_2")
            self.player.move_up()
            self.player.move_right()
        if self.hal.button_1() and self.hal.button_2():
            self.player.move_left()
            if self.player.x < 0:
                self.player.x = 0
            
    def loop(self):
        while True:
            self.hal.display.fill(0)
            # Draw landscape
            self.landscape.draw()
            self.landscape.scroll()
            
            #Enemy movement
            if random.randint(0,1) == 0:
                self.enemy.move_up()
            else:
                self.enemy.move_down()
            if self.enemy.y < 0:
                self.enemy.y = 0
            if self.enemy.y > 16:
                self.enemy.y = 16
            
            # Enemy shot
            self.shot.move_left(3)
            if self.shot.x < 0:
                self.shot.goto(100,self.enemy.y+2)
            self.shot.draw()

            self.enemy.draw()
            self.player.draw()
            
            # Collision check
            if self.player.collided == True:
                self.game_over_screen()
                
            if self.player.x == 125:
                self.game_win_screen()
                
            self.hal.display.show()
            self.control()
                
    def run(self):
        # Start screen update thread
        _thread.start_new_thread(self.loop, ())

###
hal = HAL.HAL()
sprites = Sprites("sprites.json")
game = Game(hal, sprites)
game.loop()