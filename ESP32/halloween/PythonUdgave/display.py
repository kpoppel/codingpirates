from machine import SoftI2C, Pin
import ssd1306

i2c = SoftI2C(Pin(22), Pin(21))

display = ssd1306.SSD1306_I2C(128, 32, i2c)
display.fill(1)
display.text("Coding Pirats", 10, 12, 0)
display.show()