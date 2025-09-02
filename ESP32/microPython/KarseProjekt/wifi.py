import network, time
import json

class Wifi:
    
    def __init__(self, credentials=None):
        if credentials != None:
            print("Setting up using supplied configuration")
            f = open(credentials)
            self._credentials = json.load(f)
        else:
            print("missing wifi information")

        #print(self._credentials)
        
        # Setup for client
        self.start_client()

    def start_client(self):
        station = network.WLAN(network.STA_IF)

        for x in self._credentials:
            station.active(False)
            time.sleep(2)
            station.active(True)
            self._credential=self._credentials[x]
            print('Forsøger at forbinde til lokattion: ', x)
            if station.isconnected() == False:
                #print(self._credential['ssid'], self._credential['password'])
                station.connect(self._credential['ssid'], self._credential['password'])
                
                count=0
        
                while (station.isconnected() == False) and (count < 4):
                    time.sleep(3)
                    count += 1

                    if station.isconnected() == False:
                        print('Forsøger at forbinde til: ', x)
                        
                    pass
        
        print("Connection successful")
        print(station.ifconfig())