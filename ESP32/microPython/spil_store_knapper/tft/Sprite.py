# Definition af Sprites
import json
import math

class SpriteImage:
    """
    A Sprite image.  Contains a bytearray with bitmap data, width and height and origo.
    (currently (0,0))
    Consumed by the SpriteController
    """
    def __init__(self, sprite_file_name, sprite_mask_file_name=None):
        # in_memory: Set to False if the sprite should be loaded from flash every time
        #            Useful for large sprites.
        self.sprite = None
        self.mask = None
        self.height = 0
        self.width = 0
        self.file = sprite_file_name
        self.file_mask = sprite_mask_file_name
        self.last_byte = 0
            
    def load_json(self, sprite_name):
        """ The json file loader"""
        try:
            f = open(self.file)
            sprites= json.load(f)
            f.close()
            # Space could be saved by storing data as bytearray...
            self.height = len(sprites[sprite_name])
            self.width = len(sprites[sprite_name][0])
            self.sprite = bytearray(self.height*self.width*2)
            for y, row in enumerate(sprites[sprite_name]):
                for x, data in enumerate(row):
                    if data =="1":
                        self.sprite[x*2+y*2*self.height] = 0xFF
                        self.sprite[x*2+y*2*self.height+1] = 0xFF
                    else:
                        self.sprite[x*2+y*2*self.height] = 0x00
                        self.sprite[x*2+y*2*self.height+1] = 0x00
        except:
            print("ERROR, Sprite file not found or sprite name not found.")
    
    def load_rgb565(self, from_byte=0):
        """ The RGB565 file loader"""
        fh = open(self.file, "rb")
        # Get size (seek -2 from end and read last two bytes)
        fh.seek(-2, 2)
        self.width, self.height = fh.read()
        fh.seek(from_byte, 0)
        #print(f'read from: {from_byte}')
        self.sprite = bytearray(fh.read())
        self.last_byte = self.width*self.height
        #if self.width*self.height <= 32*32:
        #    self.sprite = bytearray(fh.read())
        #    self.last_byte = self.width*self.height
        #else:
        #    self.sprite = bytearray(fh.read(1024))
        #    self.last_byte = from_byte+1024
            
    def load_rgb565_mask(self):
        """ Load a collision mask for a sprite.
            Masks are a bit-wise pixel mask of the sprite """
        fh = open(self.file_mask, "rb")
        # Get size (seek -2 from end and read last two bytes)
        fh.seek(-2, 2)
        self.mask_width, self.mask_height = fh.read()
        fh.seek(from_byte, 0)
        self.mask = bytearray(fh.read())
        # Masks are needed because the display can now contain a background image,
        # so color detection is not enough.  Masks is a monochrome version of the sprite
        # and 16 times smaller than the sprite.
        # Collision detection is potentially an expensive operation, but some optimisations
        # can be made:
        # 1) Check if the sprites is at all overlapping on a rectangular bounding box
        #    If the distance between centers of the rectangle is larger than side/2 no collision
        # 2) If overlapping just check the overlapping part
        # 2.1) if all bits are zero or only one sprite has 1's -> no collision
        # 2.2) if if both has 1's check if they are in the same position.
        
    def pixel(self, x, y):
        read_byte = 2*x+2*y*self.height
        #if read_byte == self.last_byte or read_byte == 0:
        #    #print(x,y,self.sprite)
        #    self.load_rgb565(from_byte=read_byte)
        #    print("Oh no", read_byte, x, y, self.last_byte, 2*x+2*y)
        #read_byte = 2*x+2*y
        return (self.sprite[read_byte]<<8) | self.sprite[read_byte+1]
    
class SpriteController:
    """
    A Sprite Controller.  
    """
    def __init__(self, sprite_image, framebuffer, screen_x_size, screen_y_size, keep_on_screen=True):
        self.fb = framebuffer
        self.x_max = screen_x_size
        self.y_max = screen_y_size
        
        # state:
        self.sprite = sprite_image
        self.x = 0
        self.y = 0
        self.collided = False
        self.was_off_screen = False
        self.keep_on_screen = keep_on_screen
        self._delta_x = 0
        self._delta_y = 0
        self._dir = None
        self._speed = 0

    def move_up(self, d=1):
        self.y -= d
        if self.keep_on_screen and self.off_screen():
            self.y += d
       
    def move_down(self, d=1):
        self.y += d
        if self.keep_on_screen and self.off_screen():
            self.y -= d

    def move_left(self, d=1):
        self.x -= d
        if self.keep_on_screen and self.off_screen():
            self.x += d
        
    def move_right(self, d=1):
        self.x += d
        if self.keep_on_screen and self.off_screen():
            self.x -= d
        
    def direction(self, degrees=None):
        if degrees is not None:
            # Calculate delta_x and delta_y based on direction.
            self._delta_x = math.cos(degrees/360*2*math.pi)
            self._delta_y = math.sin(degrees/360*2*math.pi)
            self._dir = degrees
        return self._dir
        
    def speed(self, speed=None):
        if speed is not None:
            self._speed = speed
        return self._speed
        
    def move(self):
        # With a direction set, just move the sprite in that direction
        # at the given speed
        self.move_up(self._delta_x*self._speed)
        off_screen = self.was_off_screen
        self.move_left(self._delta_y*self._speed)
        # Sticky off screen detection
        self.was_off_screen = off_screen or self.was_off_screen
        
    def goto(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def off_screen(self):
        self.was_off_screen = (self.x <= 0) or (self.y <= 0) or (self.x >= self.x_max - self.sprite.width) or (self.y >= self.y_max - self.sprite.height)
        return self.was_off_screen
    
    def draw(self):
        """ Render the sprite """
        self.collided = False
        x_int = int(self.x)
        y_int = int(self.y)
        for y in range(self.sprite.height):
            for x in range(self.sprite.width):
                c = self.sprite.pixel(x,y)
                if c != 0x0000:
                    self.fb.pixel(x+x_int, y+y_int, c)