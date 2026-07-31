import sys
import machine
import neopixel

LEDS = 144
LED_PIN = 47
np = neopixel.NeoPixel(machine.Pin(LED_PIN, machine.Pin.OUT), LEDS+72)

np2 = neopixel.NeoPixel(machine.Pin(48), 1)
np2[0]=[0,0,0]
np2.write()

for zyy in range(0,144+72):
    np[zyy]=(0,0,10)
np[144+72-5]=(255,0,0)
np[3]=(255,0,0)
np.write()
