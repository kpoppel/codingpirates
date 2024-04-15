#Importer nødvendige funktioner
from wifi import Wifi
from http import Http
#import time
#from handle_screen import Screen
#import HAL

wifi = Wifi("wifi-home.json")
#wifi = Wifi("wifi.json")
#wifi.start_client()
#wifi = Wifi()
http = Http()

http.start_http_server()

# Websocket
# https://staff.ltam.lu/feljc/electronics/uPython/uPy_WiFi_02.pdf
# https://staff.ltam.lu/feljc/electronics/uPython/uPy_WiFi_03.pdf
# https://github.com/jczic/MicroWebSrv?tab=readme-ov-file