import network, ntptime, time
import json

class Wifi:
    _AP_SSID = "ESP32_config"
    _AP_PASS = ""
    
    def __init__(self, credentials=None):
        if credentials != None:
            print("Setting up as WiFi client")
            f = open(credentials)
            self._credentials = json.load(f)
            print(self._credentials)
            self.start_client()
        else:
            print("Seting up as WiFi access point")
            self.start_access_point()
        pass
    
    def start_access_point(self):
        """ Start an open access point """
        AP = network.WLAN(network.AP_IF)
        AP.active(True)
        AP.config(essid=self._AP_SSID, password=self._AP_PASS, authmode=0)
        print('Connection successful')
        print(AP.ifconfig())
    
    def start_client(self):
        station = network.WLAN(network.STA_IF)
        station.active(False)
        time.sleep(1)
        station.active(True)
        station.connect(self._credentials['ssid'], self._credentials['password'])
        
        while station.isconnected() == False:
            time.sleep(2)
            pass
        
        print("Connection successful")
        print(station.ifconfig())