import neopixel
#import ssd1306
#from dfplayermini import Player
from machine import Pin
#, SoftI2C

# COPY ssd1306 and dfplayer mini to the ESP32 flash in addition to this file.

class HAL:
    """
    Abstraction of the hardware layer.
    Very simple as it does not do much to wrap drivers.

    In a professional setting the HAL layer would wrap the lower level drivers
    exposing just the functions necessary for the application.  This means
    the underlying hardware can be exchanged and only the HAL needs update.
    This is an ESP32 project with known hardware, so there is no need.
    
    use as:
      import HAL
      hal = HAL.HAL()
    """
    
    # The last two GPIOs are the on-board buttons
    BUTTON_GPIO = [13, 16, 17, 19, 27, 34, 35, 39, 12]
    BUTTON_GPIO_BOARD = [32, 33]
    LED_PIN = 0

    def __init__(self):
#        self.music = Player(pin_TX=25, pin_RX=26)
#        self.i2c = SoftI2C(Pin(22), Pin(21))
#        self.display = ssd1306.SSD1306_I2C(128, 32, self.i2c)
#        self.display.rotate(True) # screen rotation
        self.NUM_PIXELS = 3 * len(self.BUTTON_GPIO)
        self.led = neopixel.NeoPixel(Pin(self.LED_PIN), self.NUM_PIXELS)
        # Buttons connected to GPIOs:
        #  13, 16, 17, 19, 27, 34, 35, 39, 12
        #   0,  1,  2,  3,  4,  5,  6,  7,  8
        # Buttons onboard: (32, 33)
        #                    9, 10
        self.button = []
        for gpio in self.BUTTON_GPIO:
            self.button.append(Pin(gpio, Pin.IN, Pin.PULL_UP))
        self.button_board = []
        for gpio in self.BUTTON_GPIO_BOARD:
            self.button_board.append(Pin(gpio, Pin.IN, Pin.PULL_UP))

        # TFT:
        # CS: 15
        # RST: 4
        # AO:  2
        # SDA: 23
        # SCK: 18
        #spi = SPI(2, baudrate=33000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=None)
        #tft=TFT(spi=spi, aDC=2, aReset=4, aCS=15)
        #tft.initr()
        #tft.rgb(True)
        
