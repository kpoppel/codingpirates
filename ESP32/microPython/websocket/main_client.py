import asyncio
from asyncio_websockets.client import connect
from wifi import Wifi

# Connect to Wifi
wifi = Wifi("wifi-home.json")
#wifi = Wifi("wifi.json")
wifi.info()

# Test ID
test_id = 0

connected = False
ws = None
msg_data = ""

async def handle_connect():
    global connected
    global ws
    ws = await connect("ws://10.0.0.171:80/test")
    #ws = await connect("ws://10.169.172.144:80/test")
    #ws = await connect("ws://10.169.172.219:80/test")
    if not ws:
        print("connection failed")
        return
    connected = True
    print("Connected")

async def receive_data():
    """
        Modtag data fra serveren.  Gør et eller andet med det.
    """
    global ws
    global msg_data
    while connected:
        print("Connected for receive")
        async for msg in ws:
            print(msg)
            msg_data = msg

async def send_data():
    """
        Send data til  serveren.  Få serveren til at gøre noget med dem.
        Koden her sender en besked hvert sekund for at demonstrere det.
    """
    global msg_data
    global ws
    global connected
    global test_id
    while connected:
        await asyncio.sleep(1)
        await ws.send(f"OK {test_id}:{msg_data}")
        print(f"{test_id} - {msg_data}")
        test_id += 1

async def main():
    async def handler():
        """
        Coroutine to handle connection and run receive and send tasks concurrently.
        """
        connect_task = asyncio.create_task(handle_connect())
        await connect_task
        receive_task = asyncio.create_task(receive_data())
        send_task = asyncio.create_task(send_data())
        await asyncio.gather(receive_task, send_task)

    print("asyncio websocket client setup.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler())
    loop.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
