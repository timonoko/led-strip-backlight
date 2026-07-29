import sys
import machine
import neopixel
import ubinascii
import micropython

# Disable Ctrl+C interrupt so serial characters like 0x03 won't break execution
micropython.kbd_intr(-1)

LEDS = 144
LED_PIN = 47

np2 = neopixel.NeoPixel(machine.Pin(48), 1)

np = neopixel.NeoPixel(machine.Pin(LED_PIN, machine.Pin.OUT), LEDS)
print("Takavalo hex serial listener ready...")

while True:
    line = sys.stdin.readline()
    if line:
        line = line.strip()
        if line == "STOP":
            np.fill((0, 0, 0))
            np.write()
            micropython.kbd_intr(3)
            print("Received STOP. MicroPython REPL restored.")
            sys.exit()
        # 144 LEDs * 3 RGB bytes = 432 bytes = 864 hex characters
        elif len(line) == 864:
            try:
                data = ubinascii.unhexlify(line)
                for i in range(LEDS):
                    r = data[i * 3] // 5
                    g = data[i * 3 + 1] // 5
                    b = data[i * 3 + 2] // 5
                    np[i] = (r, g, b)
                np.write()
                np2[0]=[0,0,0]
                np2.write()
            except Exception:
                pass

