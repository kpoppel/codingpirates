import network, time, socket, os
import machine, neopixel
from machine import Pin, ADC
from VUmeterfl import VUmeter
import _thread

ssid = "SSIDNAME"
password = "YOUPASSWORD"

# reference konstanter
NOT_FOUND_TEMPLATE = '404.html'
TEXT_HTML = 'text/html'
TEXT_CSS = 'text/css'
TEXT_JAVASCRIPT = 'text/javascript'

# Mål strømforbrug på GPIO4
CURRENT = ADC(Pin(4))

#GPIO til LedStrip
PinNr = 16

# VUmeter er off til at starte 
VUmeterON = False
    


def StartVUmeter():
    global VUmeterON
    print ("Starter VU meter")

    while VUmeterON == True:
        VUmeter(LedCount)

#Tæl antal af Leds
def LedCounter(LedCount=0):
    #Sæt farver
    WHITE = (255, 255, 255)
    OFF = (0, 0, 0)
    
    #Start værdi til første gennemgang
    CurrentValue = 60
    
    while CurrentValue > 50:
        # Initialiser LedStrip
        LedStrip = neopixel.NeoPixel(machine.Pin(PinNr), LedCount + 1)
        
        #Tænd en hvid led
        LedStrip[LedCount] = WHITE
        LedStrip.write()
        
        #Læs strømforbrug
        CurrentValue = CURRENT.read()
        
        #Sluk Alle
        time.sleep_ms(50)
        LedStrip.fill(OFF)
        LedStrip.write()
        LedCount += 1
        
    print(LedCount - 1)
    return(LedCount -1)


# læs filer fra lokalt fil system
def get_file(filename):
    """
    Returns a file from ESP32 filesystem
    :param filename:
    :return:
    """
    try:
        filesystem = os.listdir()
        if filename not in filesystem:
            error = 'Error: ' + filename + ' file not found in root dir. Found: ' + filesystem
            print(error)
            return error  # TODO check it is safe to return a string instead of file
        file = open(filename)
        f = file.read()
        file.close()
        return f
    except Exception as e:
        return e

# connect ESP til wireless netværk
def WLClient():
    station = network.WLAN(network.STA_IF)
    station.active(False)
    time.sleep(1)
    station.active(True)
    station.connect(ssid, password)
    
    while station.isconnected() == False:
        time.sleep(2)
        pass
    
    print("Connection successful")
    print(station.ifconfig())


# Start et wireless AP
def WLAP():
    AP = network.WLAN(network.AP_IF)
    AP.active(True)
    AP.config(essid=ssid, password=password, authmode=3)
    print('Connection successful')
    print(AP.ifconfig())

def create_response(connection, filename=NOT_FOUND_TEMPLATE, content_type=TEXT_HTML):
    response = get_file(filename)
    connection.send('HTTP/1.1 200 OK\n')  # TODO write a cycle to send response page
    connection.send('Content-Type: ' + content_type + '\n')
    connection.send('Connection: close\n\n')
    connection.sendall(response)
    connection.close()

def color_read(request):
    color_request = 'GET /?color='
    red_index = request.find(color_request) + len(color_request)
    green_index = red_index + 2
    blue_index = green_index + 2
    # TODO wrap this shit into functions
    red_val = int(request[red_index:green_index], 16)
    green_val = int(request[green_index:blue_index], 16)
    blue_val = int(request[blue_index:blue_index + 2], 16)

    return red_val, green_val, blue_val


def strip_clear(strip):
    """
    Turns off all the strip LEDs
    :param strip: instance of NeoPixel led strip object (defined in `boot.py` as `led_strip` variable)
    :return: None
    """

    for i in range(LedCount):
        led_strip[i] = (0, 0, 0, 0)  # R G B W

    strip.write()


def strip_fill_color(strip=None, red=0, green=0, blue=0, white=0):
    """
    Fill all strip LEDs with defined colors
    This function is useful for setting the same color to the whole strip

    :param strip: instance of NeoPixel led strip object (defined in `boot.py` as `led_strip` variable)
    :param red: RED color value (0-255)
    :param green: GREEN color value (0-255)
    :param blue: BLUE color value (0-255)
    :param white: WHITE color value (0-255)
    :return: None
    """
    if strip is None:
        strip = NeoPixel(LED_PIN, LedCount, bpp=4)
        
    print(red, green, blue, white)

    for i in range(LedCount):
        led_strip[i] = (red, green, blue, white)

    strip.write()

def wheel(pos):
    """
    Wheel is a width of a single rainbow line

    Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r.
    """
    if pos < 0 or pos > 255:
        return 0, 0, 0, 0
    if pos < 85:
        # TODO add incoming commands check while spinning rainbow wheel
        return 255 - pos * 3, pos * 3, 0, 0
    if pos < 170:
        pos -= 85
        return 0, 255 - pos * 3, pos * 3, 0
    pos -= 170
    return pos * 3, 0, 255 - pos * 3, 0


def rainbow_cycle(wait=0):
    for j in range(256):
        for i in range(LedCount):
            rc_index = (i * 256 // LedCount) + j
            led_strip[i] = wheel(rc_index & 255)
        led_strip.write()
        if wait > 0:
            time.sleep_ms(wait)  # change to remove sleep


def http_server():
    global VUmeterON
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 80))
    sock.listen(5)
    
    while True:
      client, addr = sock.accept()
      print('Client %s is connected' % str(addr))
      request = client.recv(1024)
      request = str(request)
      Led_off = False
      led_on = request.find('/?color=000000ff')
      print ("led_on:", led_on)
      led_off = request.find('/?color=00000000')
      led_rainbow = request.find('/?led=rainbow')
      led_medium = request.find('/?color=00000096')
      print ("med:", led_medium)
      led_low = request.find('/?color=00000032')
      vumeter = request.find('/?led=vumeter')
      
      if vumeter == 6:
          print('VU Meter')
          VUmeterON = True
          _thread.start_new_thread(StartVUmeter, ())
          
      if led_rainbow == 6:
          print('RAINBOW MODE')
          rainbow_cycle()
      if led_medium == 6:  # TODO wrap state check into separate function
          print('LED MEDIUM')
          strip_fill_color(led_strip, 127, 0, 0, 150)
          time.sleep(2)
      if led_low == 6:
          print('LED LOW')
          strip_fill_color(led_strip, 64, 0, 0, 50)
      if led_on == 6:
          print('LED ON')
          strip_fill_color(led_strip, 255, 0, 0, 255)
      if led_off == 6:
          print('LED OFF')
          strip_clear(led_strip)
          VUmeterON = False


      if request.find('GET /style.css', 2, 17) >= 0:
          create_response(client, 'style.css', TEXT_CSS)
      elif request.find('GET /functions.js', 2, 20) >= 0:
          create_response(client, 'functions.js', TEXT_JAVASCRIPT)
      elif request.find('GET /jscolor.min.js', 2, 22) >= 0:
          create_response(client, 'jscolor.min.js', TEXT_JAVASCRIPT)
      elif request.find('GET /?color=', 2, 19) >= 0:
          # TODO get colorsting into variable
          rgb = color_read(request)
          print(rgb)
          if rgb != (0, 0, 0) or Led_off == 6:
              strip_fill_color(led_strip, *rgb)
          create_response(client, 'index.html', TEXT_HTML)
      else:
          create_response(client, 'index.html', TEXT_HTML)


LedCount=LedCounter()
print("Antal Leds", LedCount)
led_strip = neopixel.NeoPixel(machine.Pin(PinNr), LedCount)

# connect til wireless. Vælg kun WLClient eller AP ikke begge dele
WLClient()

#start et wireless AP. Vælg kun WLClient eller AP ikke begge dele
#WLAP()

http_server()
