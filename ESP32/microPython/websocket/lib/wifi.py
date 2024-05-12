# Wifi class
#
# Setup WiFi connection as access point (AP) or client (STA)
#
# Use:
# from wifi import WiFi
# wifi = Wifi(credentials="path/file.json", debug=False)
#
# The path/file.json format is:
#
# {
#    "use": "AP|STA",
#     "AP": {
#            "ssid": "EGE-Internet",
#            "password": ""
#          },
#     "STA": {
#            "ssid": "EGE-Internet",
#            "password": ""
#          }
# }
#
# Set "use" to AP or STA to select connection type.
#
import network, time, json

class Wifi:
    _SSID = "ESP32_config"
    _PASS = "config"
    _TYPE = "STA"
    
    def __init__(self, credentials=None):
        self.connection = None
        if credentials != None:
            f = open(credentials)
            credentials = json.load(f)
            self._TYPE = credentials['use']
            self._SSID = credentials[self._TYPE]['ssid']
            self._PASS = credentials[self._TYPE]['password']

            if self._TYPE == "STA":
                self.start(network.STA_IF)
            else:
                self.start(network.AP_IF)
        
    def start(self, type):
        self.connection = network.WLAN(type)
        self.connection.active(False)
        time.sleep_ms(250)
        self.connection.active(True)
        if self._TYPE == "STA":
            self.connection.connect(self._SSID, self._PASS)
            while self.connection.isconnected() == False:
                time.sleep_ms(250)
        else:
            self.connection.config(ssid=self._SSID, key=self._PASS)
         
    def info(self):
        print(self.connection.ifconfig())
