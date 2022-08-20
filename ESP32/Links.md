# Gode links

Her kan pinout på ESP32 modulet ses, samt en del kodeeksempler
https://wolles-elektronikkiste.de/en/programming-the-esp32-with-arduino-code

# USB HID modul
 https://blog.drorgluska.com/2017/07/rc-joystick-with-frsky-dht-module-and.html
 https://www.state-of-the-art.io/projects/pianolights/ (ESP32 diagram)
 
 Tilføj library: USB-Host-Shield-20 by Oleg Mazurov
 https://github.com/felis/USB_Host_Shield_2.0
 
 Silketryk bag på USB modul er forkert: https://forum.pjrc.com/attachment.php?attachmentid=10950&d=1499204773
 
# Introduktion SPI på ESP32
 https://randomnerdtutorials.com/esp32-spi-communication-arduino/
 
# Hvis man har flere ESPere forbundet til sin computer?
Så skifter COM porte rundt.  Hvilke der findes, kan ses sådan her:
https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/establish-serial-connection.html
Højreklik på "Windows" -> Enhedshåndtering -> porte COM3, COM4, COM5 er ikke unormalt at se

# ESP8266 som logikanalysator (en dårlig en)
Download https://processing.org/donate
Download https://github.com/aster94/logic-analyzer
Upload med Arduino studio.
Forbind testledninger til D1, D2, D5, D6 på ESP8266 board og til målepunkter.
Ubrugte pins skal sættes til GND
 
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


# ESP32 i Arduino Studio
https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/
