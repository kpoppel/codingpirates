# Inspireret bl.a. af kode fra: https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
import time
import machine, neopixel

# Fortæl programmet hvor mange LED på strip:
NUM_PIXELS = 10
# Fortæl programmet hvilken GPIO data-pin er sat på:
PIN = 26

def rainbow_v1(np, repeat=300):
    # simpel regnbue
    print("Regnbue V1 - 32 farver forudbestemt")
    rainbow = [
      (126 , 1 , 0),(114 , 13 , 0),(102 , 25 , 0),(90 , 37 , 0),(78 , 49 , 0),(66 , 61 , 0),(54 , 73 , 0),(42 , 85 , 0),
      (30 , 97 , 0),(18 , 109 , 0),(6 , 121 , 0),(0 , 122 , 5),(0 , 110 , 17),(0 , 98 , 29),(0 , 86 , 41),(0 , 74 , 53),
      (0 , 62 , 65),(0 , 50 , 77),(0 , 38 , 89),(0 , 26 , 101),(0 , 14 , 113),(0 , 2 , 125),(9 , 0 , 118),(21 , 0 , 106),
      (33 , 0 , 94),(45 , 0 , 82),(57 , 0 , 70),(69 , 0 , 58),(81 , 0 , 46),(93 , 0 , 34),(105 , 0 , 22),(117 , 0 , 10)]

    for times in range(repeat):
        rainbow = rainbow[-1:] + rainbow[:-1]
        for i in range(np.n):
            np[i] = rainbow[i]
        np.write()
        time.sleep_ms(30)

def rainbow_v2(np, step=32, repeat=1024):
    # Denne version tager en del hukommelse, da alle tal ((256*6)/step byte) gemmes i et array
    # Jo høre steps er mellem farver, des mindre RAM bruger denne version godt nok.
    rainbow = []
    print("Regnbue V2 - RAM:", 2*3*256//step, "Bytes")
    for r, g, b in zip(
            ( [255] * (256//step) +
              list(reversed(range(0,256,step))) +
              [0] * (256//step) +
              [0] * (256//step) +
              list(range(0,256,step)) +
              [255] * (256//step)
            ),
            ( list(range(0,256,step)) +
              [255] * (256//step) +
              [255] * (256//step) +
              list(reversed(range(0,256,step))) +
              [0] * (256//step) +
              [0] * (256//step)
            ),
            ( [0] * (256//step) +
              list(range(0,256,step)) +
              [255] * (256//step) +
              [255] * (256//step) +
              list(reversed(range(0,256,step)))
            )
        ):
        rainbow.append((r, g, b))

    for times in range(repeat):
        rainbow = rainbow[-1:] + rainbow[:-1]
        for i in range(np.n):
            np[i] = rainbow[i]
        np.write()
        time.sleep_ms(30)

def rainbow_v3(np, step=32, max_intensity=256, repeat=1024):
    print("Regnbue V3 - RAM: 20 Bytes")
    # Denne version bruger mindre RAM end v2.  Næste farve beregnes og kun
    # neopixels opdateres.
    speed = 1*(256 // max_intensity)*step
    state = 0
    rb = [(0,0,0)]*10
    r = max_intensity
    g = 0
    b = 0
    for times in range(repeat):
        if state == 0:
            # Grøn op, rød=max, blå=0
            g += step
            if g == max_intensity:
                state = 1
        if state == 1:
            # Grøn max, Rød ned, blå=0
            r -= step
            if r == 0:
                state = 2
        if state == 2:
            # Grøn max, rød=0, Blå op
            b += step
            if b == max_intensity:
                state = 3
        if state == 3:
            # Grøn ned, rød=0, Blå=max
            g -= step
            if g == 0:
                state = 4
        if state == 4:
            # Grøn=0, Rød op, Blå=max
            r += step
            if r == max_intensity:
                state = 5
        if state == 5:
            # Grøn=0, rød=max, Blå ned
            b -= step
            if b == 0:
                state = 0
        
        # Denne linje tager f.eks.: [(1,1,1),(2,2,2)] -> [(2,2,2),(r,g,b)]
        rb = rb[1:] + [(min(r, 255),min(g,255),min(b,255))]
        # Send det hele til LED strip
        for i in range(np.n):
            np[i] = rb[i]
        np.write()
        time.sleep_ms(speed)

def cycle(np):
    n = np.n
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

def bounce_v1(np):
    n = np.n
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)
       
def fade_in_out(np):
    n = np.n
    for i in range(0, 8 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            # Skift farve hver gang der fades ind
            if i<512:
                np[j] = (val, 0, 0)
            elif i<1024:
                np[j] = (val, val, 0)
            elif i<1536:
                np[j] = (0, val, val)
            else:
                np[j] = (0, 0, val)
        np.write()
        time.sleep_ms(30)

def off(np):
    # Sluk for alle LEDs
    n = np.n
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

np = neopixel.NeoPixel(machine.Pin(PIN),NUM_PIXELS)

# DEMO TIME
cycle(np)
bounce_v1(np)
fade_in_out(np)
rainbow_v1(np)
rainbow_v2(np, repeat=512)
rainbow_v3(np, repeat=512)
off(np)