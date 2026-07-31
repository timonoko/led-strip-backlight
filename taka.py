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

np = neopixel.NeoPixel(machine.Pin(LED_PIN, machine.Pin.OUT), LEDS+72)
print("Takavalo hex serial listener ready...")

prevcolo=(10000,10000,10000)

while True:
    line = sys.stdin.readline()
    if line:
        line = line.strip()
        if line == "STOP":
#            np.fill((0, 0, 0))
#            np.write()
            micropython.kbd_intr(3)
            print("Received STOP. MicroPython REPL restored.")
            sys.exit()
        # 144 LEDs * 3 RGB bytes = 432 bytes = 864 hex characters
        elif len(line) == 864:
            try:
#               himmennys=5*144
#               prevcolo=(prevcolo[0]//himmennys,prevcolo[1]//himmennys,prevcolo[2]//himmennys)
                for zyy in range(144,144+72):
                     np[zyy]=(0,0,10)
                np[144+72-5]=(255,255,255)
#                    np[zyy]=prevcolo
#                prevcolo=(0,0,0)
                data = ubinascii.unhexlify(line)
                for i in range(LEDS):
                    r = data[i * 3] // 7
                    g = data[i * 3 + 1] // 7
                    b = data[i * 3 + 2] // 7
#                    prevcolo=(prevcolo[0]+r,prevcolo[1]+g,prevcolo[2]+b)
                    np[i] = (r, g, b)
                np.write()
                np2[0]=[0,0,0]
                np2.write()
            except Exception:
                print('erhe',prevcolo)
                pass

