## SDCARD setup:
#   https://www.youtube.com/watch?v=rq5yPJbX_uk&t=446s

from st7735 import TFT, TFTColor
from sysfont import sysfont
from machine import SPI,Pin
import time
import math
import random

# TFT initialisering
spi = SPI(2, baudrate=33000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=None)
print(spi)
tft=TFT(spi=spi, aDC=2, aReset=4, aCS=15)
#tft=TFT(spi=spi, aDC=2, aReset=4, aCS=5)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

from framebuf import FrameBuffer, RGB565
buf = bytearray(128*160*2)
fb = FrameBuffer(buf, 128, 160, RGB565)
palb = bytearray(128*1*2)
pal = FrameBuffer(palb, 1,128,RGB565)

def test_framebuffer(size=20, repeat=1000):
    tft._setwindowloc((0,0),(127,159))

    (xmax, ymax) = (128-size, 160-size)
    (x, y) = (size, size)
    (vx, vy) = (1, 1)

    for n in range(repeat):
        fb.fill(0)
        fb.ellipse(x, y, size, size, TFTColor(0xff, 0xff, 0xff), True)
#        fb.ellipse(x, y, size, size, 0xffff, True)
        x += vx
        if x == xmax or x == size:
            vx = -vx
        y += vy
        if y == ymax or y == size:
            vy = -vy
        tft._writedata(buf)

while True:
    test_framebuffer()

def plasma(w=128,h=160):
    for x in range(0, w):
        for y in range(0, h):
            color = int(((128+(128*math.sin(x/32.0)))
                +(128+(128*math.cos(y/32.0))) 
                +(128+(128*math.sin(math.sqrt((x*x+y*y))/32.0))))/4)
#            tft.pixel(aPos=(x,y), aColor=color)
            fb.pixel(x, y, color&255)
    tft._writedata(buf)

    frameCount = 0
    r = 27
    g = 34
    b = 117
    rd = False
    gd = False
    bd = False
    
    while True:
        if r > 128:
            rd = True
        if not rd:
            r+=3
        else:
            r-=3
        if r < 0:
            rd = False
        if g > 128:
            gd = True
        if not gd:
            g+=3
        else:
            g-=3
        if r < 0:
            gd = False
        if b > 128:
            bd = True
        if not bd:
            b+=3
        else:
            b-=3
        if (b < 0):
            bd = False

        #pal = [0] * 128
        for i in range(0, 128):
            s_1 = math.sin(i*math.pi/25);
            s_2 = math.sin(i*math.pi/50+math.pi/4);
#            pal[i] = TFTColor(int(r+s_1*128), int(g+s_2*128), int(b+s_1*128))
            pal.pixel(i,0, TFTColor(int(r+s_1*128), int(g+s_2*128), int(b+s_1*128)))

        for x in range(0, w):
            for y in range(0, h):
#                 color = int(((128+(128*math.sin(x/32.0)))
#                     +(128+(128*math.cos(y/32.0))) 
#                     +(128+(128*math.sin(math.sqrt((x*x+y*y))/32.0))))/4)
    #             color = TFTColor(int( 128+(128*math.sin(x/32.0) ) ),
    #                              int( 128+(128*math.cos(y/32.0))  ),
    #                              int( 128+(128*math.sin(math.sqrt(x*x+y*y)/32.0))/4 )
    #                              )
                
                #tft.pixel(aPos=(x,y), aColor=(color+frameCount)&255)
#                fb.pixel(x, y, (color+frameCount)&255)
                #fb.pixel(x, y, pal[x])
                fb.blit(fb, x, y, -1, pal)

        tft._writedata(buf)

plasma()

def all_colors():
    for r in range(0,256):
        for g in range(0,256):
            for b in range(0,256):
                tft.fill(TFTColor(r, g, b))

def testlines(color):
    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((0,0),(x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((0,0),(tft.size()[0] - 1, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, 0), (x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, 0), (0, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((0, tft.size()[1] - 1), (x, 0), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((0, tft.size()[1] - 1), (tft.size()[0] - 1,y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, tft.size()[1] - 1), (x, 0), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, tft.size()[1] - 1), (0, y), color)

def testfastlines(color1, color2):
    tft.fill(TFT.BLACK)
    for y in range(0, tft.size()[1], 5):
        tft.hline((0,y), tft.size()[0], color1)
    for x in range(0, tft.size()[0], 5):
        tft.vline((x,0), tft.size()[1], color2)

def testdrawrects(color):
    tft.fill(TFT.BLACK);
    for x in range(0,tft.size()[0],6):
        tft.rect((tft.size()[0]//2 - x//2, tft.size()[1]//2 - x/2), (x, x), color)

def testfillrects(color1, color2):
    tft.fill(TFT.BLACK);
    for x in range(tft.size()[0],0,-6):
        tft.fillrect((tft.size()[0]//2 - x//2, tft.size()[1]//2 - x/2), (x, x), color1)
        tft.rect((tft.size()[0]//2 - x//2, tft.size()[1]//2 - x/2), (x, x), color2)


def testfillcircles(radius, color):
    for x in range(radius, tft.size()[0], radius * 2):
        for y in range(radius, tft.size()[1], radius * 2):
            tft.fillcircle((x, y), radius, color)

def testdrawcircles(radius, color):
    for x in range(0, tft.size()[0] + radius, radius * 2):
        for y in range(0, tft.size()[1] + radius, radius * 2):
            tft.circle((x, y), radius, color)

def testtriangles():
    tft.fill(TFT.BLACK);
    color = 0xF800
    w = tft.size()[0] // 2
    x = tft.size()[1] - 1
    y = 0
    z = tft.size()[0]
    for t in range(0, 15):
        tft.line((w, y), (y, x), color)
        tft.line((y, x), (z, x), color)
        tft.line((z, x), (w, y), color)
        x -= 4
        y += 4
        z -= 4
        color += 100

def testroundrects():
    tft.fill(TFT.BLACK);
    color = 100
    for t in range(5):
        x = 0
        y = 0
        w = tft.size()[0] - 2
        h = tft.size()[1] - 2
        for i in range(17):
            tft.rect((x, y), (w, h), color)
            x += 2
            y += 3
            w -= 4
            h -= 6
            color += 1100
        color += 100

def tftprinttest():
    tft.fill(TFT.BLACK);
    v = 30
    tft.text((0, v), "Hello World!", TFT.RED, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0, v), "Hello World!", TFT.YELLOW, sysfont, 2, nowrap=True)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Hello World!", TFT.GREEN, sysfont, 3, nowrap=True)
    v += sysfont["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, sysfont, 4, nowrap=True)
    time.sleep_ms(1500)
    tft.fill(TFT.BLACK);
    v = 0
    tft.text((0, v), "Hello World!", TFT.RED, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), str(math.pi), TFT.GREEN, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " Want pi?", TFT.GREEN, sysfont)
    v += sysfont["Height"] * 2
    tft.text((0, v), hex(8675309), TFT.GREEN, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " Print HEX!", TFT.GREEN, sysfont)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Sketch has been", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), "running for: ", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), str(time.ticks_ms() / 1000), TFT.PURPLE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " seconds.", TFT.WHITE, sysfont)

def test_random():
    xw = tft.size()[0]
    yw = tft.size()[1]
    data = bytearray(xw*yw*2)
    t1 = time.ticks_us()
#    for x in range(xw):
#        for y in range(yw):
#            data[x*xw+y] = random.randint(0,32768)
    r=255
    g=255
    b=255
    for d in range(0,len(data),2):
        data[d] = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        #data[d] = 0x127#31 # green
        #data[d+1] = 0#31 blue
    t2 = time.ticks_us()
    print("Data",(t2-t1)/1000,"ms")

    # push the pixels and time
    #tft.fill(TFT.BLACK)
    i=0
    #tft._writedata(data)
    t1 = time.ticks_us()
    x0=0
    y0=0
    x1=xw
    y1=yw
    tft.image(x0, y0, x1, y1, data)
#     x0=0
#     y0=128
#     x1=xw
#     y1=yw+128
#     tft.image(x0, y0, x1, y1, data)
#     for x in range(xw):
#         for y in range(yw):
# #             tft.pixel(aPos=(x,y), aColor=data[x*128+y])
#             #tft.pixel(aPos=(x,y), aColor=data[i])
#             tft._setwindowpoint( (x,y))
#             tft._pushcolor( data[i] )
#             
#             i+=1
    t2 = time.ticks_us()
    print((t2-t1)/1000,"ms")
    
    
def test_main():
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur adipiscing ante sed nibh tincidunt feugiat. Maecenas enim massa, fringilla sed malesuada et, malesuada sit amet turpis. Sed porttitor neque ut ante pretium vitae malesuada nunc bibendum. Nullam aliquet ultrices massa eu hendrerit. Ut sed nisi lorem. In vestibulum purus a tortor imperdiet posuere. ", TFT.WHITE, sysfont, 1)
    time.sleep_ms(1000)

    tftprinttest()
    time.sleep_ms(4000)

    testlines(TFT.YELLOW)
    time.sleep_ms(500)

    testfastlines(TFT.RED, TFT.BLUE)
    time.sleep_ms(500)

    testdrawrects(TFT.GREEN)
    time.sleep_ms(500)

    testfillrects(TFT.YELLOW, TFT.PURPLE)
    time.sleep_ms(500)

    tft.fill(TFT.BLACK)
    testfillcircles(10, TFT.BLUE)
    testdrawcircles(10, TFT.WHITE)
    time.sleep_ms(500)

    testroundrects()
    time.sleep_ms(500)

    testtriangles()
    time.sleep_ms(500)

tft.rgb(False)
for i in range(10):
    test_random()

#test_main()
