# Gode links

Her kan pinout på modulet ses, samt en del kodeeksempler
https://wolles-elektronikkiste.de/en/programming-the-esp32-with-arduino-code

USB HID modul:
 https://blog.drorgluska.com/2017/07/rc-joystick-with-frsky-dht-module-and.html
 https://www.state-of-the-art.io/projects/pianolights/ (ESP32 diagram)
 
 Tilføj library: USB-Host-Shield-20 by Oleg Mazurov
 
# VSCode

platform.io installeres
Espressif32 platform installeres
Brug board "A-Z delivery"

RGB pixels: tilføj "Adafruit NeoPixel" library.
  Eksempelprogrammet skal lige omorganiseres så funktioner ligger før de bruges.
  
Display: tilføj "U8g2" ilbrary.
  Eksempel-program:
  https://www.az-delivery.de/en/blogs/azdelivery-blog-fur-arduino-und-raspberry-pi/platformio-erste-schritte
  
Button presses: tilføj "AceButton" library.
  Biblioteket håndterer debounce mv.
  
Tråde:
