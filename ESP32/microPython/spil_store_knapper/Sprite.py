# Definition af Sprites
import json

class Sprite:
    """
    A Sprite.  Origo for the Sprite is upper left corner.
    TODO: Add configuration to keep on screen and so on
    """
    def __init__(self, display, sprite_file_name, sprite_name):
        self.display = display
        
        try:
            f = open(sprite_file_name)
            sprites= json.load(f)
            f.close()
            # Space could be saved by storing data as bytearray...
            self.sprite = sprites[sprite_name]
        except:
            print("ERROR, Sprite file not found or sprite name not found.")
        
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
        
    def off_screen(self):
        #print((self.x == 0), (self.y == 0), (self.x == self.display.width-self.w), (self.y == self.display.height-self.h))
        return (self.x == 0) or (self.y == 0) or (self.x == self.display.width-self.w) or (self.y == self.display.height-self.h)
    
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
    
