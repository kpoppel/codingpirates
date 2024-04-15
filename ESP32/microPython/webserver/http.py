"""
HTTP class inheriting from the HttpBase class.
Implements the request handler.
"""
from HttpBase import HttpBase

class Http(HttpBase):
    def handle(self):
        request = self._request
#           Led_off = False
#           led_on = request.find('/?color=000000ff')
#           print ("led_on:", led_on)
#           led_off = request.find('/?color=00000000')
#           led_rainbow = request.find('/?led=rainbow')
#           led_medium = request.find('/?color=00000096')
#           print ("med:", led_medium)
#           led_low = request.find('/?color=00000032')
#           vumeter = request.find('/?led=vumeter')
          
#           if vumeter == 6:
#               print('VU Meter')
#               VUmeterON = True
#               _thread.start_new_thread(StartVUmeter, ())
#               
#           if led_rainbow == 6:
#               print('RAINBOW MODE')
#               rainbow_cycle()
#           if led_medium == 6:  # TODO wrap state check into separate function
#               print('LED MEDIUM')
#               strip_fill_color(led_strip, 127, 0, 0, 150)
#               time.sleep(2)
#           if led_low == 6:
#               print('LED LOW')
#               strip_fill_color(led_strip, 64, 0, 0, 50)
#           if led_on == 6:
#               print('LED ON')
#               strip_fill_color(led_strip, 255, 0, 0, 255)
#           if led_off == 6:
#               print('LED OFF')
#               strip_clear(led_strip)
#               VUmeterON = False

        if request.find('GET /style.css', 2, 17) >= 0:
            create_response('style.css', self.TEXT_CSS)
        elif request.find('GET /functions.js', 2, 20) >= 0:
            create_response('functions.js', self.TEXT_JAVASCRIPT)
        elif request.find('GET /jscolor.min.js', 2, 22) >= 0:
            create_response('jscolor.min.js', self.TEXT_JAVASCRIPT)
#           elif request.find('GET /?color=', 2, 19) >= 0:
#               # TODO get colorsting into variable
#               rgb = color_read(request)
#               print(rgb)
#               if rgb != (0, 0, 0) or Led_off == 6:
#                   strip_fill_color(led_strip, *rgb)
#               create_response(client, 'index.html', self.TEXT_HTML)
        else:
            self.create_response('index.html', self.TEXT_HTML)