from st7735 import TFT, TFTColor
from machine import SPI,Pin, ADC
import time
from servo import Servo
import random

class HAL():
    def __init__(self):
        self.spi = SPI(2, baudrate=33000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=None)
        print(self.spi)

        self.tft=TFT(spi=self.spi, aDC=2, aReset=4, aCS=15)
        self.tft.initr()
        self.tft.rgb(True)
        self.tft.fill(TFT.BLACK)

        self.sensor = ADC(Pin(36))
        #+----------+-------------+-----------------+
        #|          | attenuation | suggested range |
        #|    SoC   |     (dB)    |      (mV)       |
        #+==========+=============+=================+
        #|          |       0     |    100 ~  950   |
        #|          +-------------+-----------------+
        #|          |       2.5   |    100 ~ 1250   |
        #|   ESP32  +-------------+-----------------+
        #|          |       6     |    150 ~ 1750   |
        #|          +-------------+-----------------+
        #|          |      11     |    150 ~ 2450   |
        #+----------+-------------+-----------------+
        #self.sensor.atten(ADC.ATTN_11DB)
        self.sensor.atten(ADC.ATTN_2_5DB)
        #self.sensor.atten(ADC.ATTN_0DB)

        self.xservo = Servo(pin_id=32)
        self.yservo = Servo(pin_id=33)
        
        self.xservo.write(10)
        self.yservo.write(0)
        time.sleep(0.5)

class Camera():    
    def __init__(self, hal):
        # Hardware
        self.hal = hal
        
        # Grænser for optagede pixels
        self.min_y = 0
        self.max_y = 45
        self.min_x = 10
        self.max_x = 170

        self.max_value = 0
        self.min_value = 4096
        
        self.num_samples = 10
        
        # Billede
        self.pixels = [0]*(self.max_y-self.min_y)*(self.max_x-self.min_x)
        
    def set_min_max(self, v):        
        if v < self.min_value:
            self.min_value = v
        elif v > self.max_value:
            self.max_value = v

    def normalise_256(self, v, min=0, max=4096):
        """ Tag en værdi på en tallinje fra a;b og beregn en ny talværdi
            på en ny tallinje 0;255
            Tallinjen a;b 
        """
        # Undgå negative min-værdier
        if v < min:
            min = v
        return 255-(int( (v-min) / (1+max-min) * 255))

    def sample(self, num_samples=1):
        #samples = [0]*num_samples
        #v = sum([self.hal.sensor.read() for v in range(num_samples)])
        #return int(v / num_samples)
    
        v = 0
        for v in range(num_samples):
            v += self.hal.sensor.read()
        print(v, num_samples, int(v / num_samples))
        return int(v / num_samples)        

    def take_picture(self):
        for y in range(self.min_y, self.max_y):
            self.hal.yservo.write(y)
            for x in range(self.min_x, self.max_x):
                time.sleep(0.01)
                self.hal.xservo.write(x)
                v = self.sample(self.num_samples)
                # Gem sampleværdi
                #print(y*(MAX_X-MIN_X)+x-MIN_X)
                self.pixels[y*(self.max_x-self.min_x)+x-self.min_x] = v
                self.set_min_max(v)
                print(self.min_value, self.max_value)
#                val = self.normalise_256(v, self.min_value, self.max_value-self.min_value)
                val = self.normalise_256(v, self.min_value, self.max_value)
                print(f"{v} : [{self.min_value}:{self.max_value}], norm={val}")

                self.hal.tft.pixel((y+10,x-10), TFTColor(val, val, val))
            self.hal.xservo.write(10)
            time.sleep(0.5)

    def normalise_picture(self, min_value=None, max_value=None):
        if min_value == None:
            min_value = self.min_value
        if max_value == None:
            max_value = self.max_value
            
        pixels = ([self.normalise_256(v, min_value, max_value) for v in self.pixels])
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                pixel = self.pixels[y*(self.max_x-self.min_x)+x-self.min_x]
                self.hal.tft.pixel((y+10,x-10), TFTColor(pixel, pixel, pixel))
        return pixels

    def generate_test_picture(self, min_val, max_val):
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                v = random.randint(min_val, max_val)
                self.pixels[y*(self.max_x-self.min_x)+x-self.min_x] = v
                self.set_min_max(v)
                val = self.normalise_256(v)
                #print(f"{v} : [{self.min_value}:{self.max_value}], norm={val}")
                self.hal.tft.pixel((y+10,x-10), TFTColor(val, val, val))
        
# Beregning af ideel modstand til spændingsdeler.
# Fotomodstanden skal udmåles i lys og mørke der
# passer med der hvor der skal tages billeder.
# Prøv Rtop modstande, der ligger i nærheden af
# fotomodstandens værdi i mørke.
def voltage_divider(Rtop, Rbottom, Vin=3.3):
    return Rbottom/(Rtop+Rbottom)*Vin

# Min modstand:
#  1MOhm max modstand i mørke
#  1kOhm min modstand i direkte lys
#
#  Ved stuelys og lys fra monitor:
#  700k-450k
print(voltage_divider(Rtop=1100e3, Rbottom=700e3))
print(voltage_divider(Rtop=1100e3, Rbottom=100e3))


#while True:
#    v = sample(10)
#    set_min_max(v)
#    val = normalise_256(v, offset=min_value, divider=max_value-min_value)
#    print(f"{v} : [{min_value}:{max_value}], norm={val}")
#    
#exit()


if __name__ == "__main__":
    hal = HAL()
    camera = Camera(hal)
    #camera.generate_test_picture(0, 700)
    #camera.min_value = 0
    #camera.max_value = 700
    camera.take_picture()
    camera.normalise_picture()
    
print("done")