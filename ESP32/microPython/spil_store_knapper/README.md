Programmerne *led* kan køres enkeltvis fra Thonny.

Programmerne der bruger OLED eller TFT diplays skal uploades til ESP32 sådan her:
    
sprites.json til /
HAL.py til /

Hvis man bruger OLED display, skal Sprite.py kopieres til /
Hvis man bruger TFT display, skal alle filer i tft/ kopieres til /  De overskriver oled-udgaverne

TFT-display-udgaven kan køres hvis programmer ligger som "main.py".  Der sker så meget, at
debugger/REPL ikke kan nå at køre hvis programmet kopieres fra Thonny. Brug ctrl-C til at stoppe programmet.


Billeder/sprites skal konverteres til bytearrays med 8bit RGB farver inden de kan bruges.
Design en sprite med: https://www.pixilart.com/draw#
Konverter den til hex med:

https://github.com/jyvet/pic2oled

En mere letvægt ST7735 driver?
  https://github.com/antirez/ST77xx-pure-MP?tab=readme-ov-file
  
Skal der spares lidt hukommelse?
http://bukys.eu/blog/230129_mpy-cross_the_ultimate_micropython_precompilation_tool._download_available
Kør som:
  mpy_cross -O3 <pythonfil>

Hurtigere/mindre TFT driver:
https://github.com/antirez/ST77xx-pure-MP?tab=readme-ov-file
