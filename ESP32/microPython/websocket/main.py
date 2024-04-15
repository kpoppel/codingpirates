# Microdot manual:
# https://microdot.readthedocs.io/en/latest/intro.html

import _thread
from wifi import Wifi
from microdot import Microdot, send_file
from microdot.websocket import with_websocket

wifi = Wifi("wifi-home.json")
#wifi = Wifi("wifi.json")

app = Microdot()

#@app.route('/')
#async def index(request):
#    return 'Hello, world!'

@app.route('/')
async def index(request):
    return send_file('index.html')


@app.route('/echo')
@with_websocket
async def echo(request, ws):
    while True:
        data = await ws.receive()
        await ws.send(data)
        
print("Running app")
#_thread.start_new_thread(app.run, (), {'port':80})

app.run(port=80)
print("App Running")

print()
