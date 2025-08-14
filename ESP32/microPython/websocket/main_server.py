import ssd1306
import asyncio

from wifi import Wifi
from machine import SoftI2C, Pin
from asyncio_websockets.server import serve

# Connect to Wifi
#wifi = Wifi("wifi.json")
wifi = Wifi("home.json")
wifi.info()

# Setup oled display
i2c = SoftI2C(Pin(22), Pin(21))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
lines = ["", "", "", ""]

# Setup pirate board buttons
knap1 = Pin(32, Pin.IN, Pin.PULL_UP)
knap2 = Pin(33, Pin.IN, Pin.PULL_UP)
    
def write(text):
    """ Use oled display for logging lines of text """
    global line_ptr
    display.fill(1)
    # cycle text
    lines[0] = lines[1]
    lines[1] = lines[2]
    lines[2] = lines[3]
    lines[3] = text
    for idx in range(0,4):
        display.text(lines[idx], 0, 8*idx, 0)
    display.show()

# Register last button pressed. '1' means not pressed (PULLUP)
last_button = 3

async def handle_connect(ws,path):
    # ws is a WebSocketServer instance
    print("Connection on {}".format(path))
    write("Ny forbindelse")
    await ws.send("Welcome client to {}".format(path))

async def receive_data(ws, path):
    """
       Her kan vi modtage data fra klienten uafhængigt af de data vi sender.
       Brug data modtaget til at gøre noget, f.eks. skifte farver på de store knapper.
    """
    async for msg in ws:
        print(msg)
        write(msg)
   
async def send_data(ws, path):
    global last_button

    """
        Scan knapperne og send status til klienten hvis den har ændret sig.
        Hvis knapperne ikke har ændret sig så skal funktionen give plads til
        noget andet. Det gør vi med asyncio.sleep(0).
    """
    while True:
        try:
            button = str(knap1() | knap2() << 1)
            if button != last_button:
                write(f"Btn {last_button}->{button}")
                last_button = button
                await ws.send(button)
            else:
                await asyncio.sleep(0)
        except:
            print("Connection reset")

async def main():
    async def handler(ws, path):
        """
        Coroutine to handle incoming connection and run receive and send tasks concurrently.
        """
        connect_task = asyncio.create_task(handle_connect(ws, path))
        receive_task = asyncio.create_task(receive_data(ws, path))
        send_task = asyncio.create_task(send_data(ws, path))
        await asyncio.gather(connect_task, receive_task, send_task)

    server = serve(handler, "0.0.0.0", 80)
    #ws_server = serve(asyncio.coroutine(hhandler), "0.0.0.0", 80)

    print("Server listening on 0.0.0.0:80")
    write("Websocket klar")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server)
    loop.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
