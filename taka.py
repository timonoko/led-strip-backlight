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

flag=0

while True:
    line = sys.stdin.readline()
    if line:
        line = line.strip()
        if line == "STOP":
            micropython.kbd_intr(3)
            print("Received STOP. MicroPython REPL restored.")
#            sys.exit()
            machine.reset()
        # 144 LEDs * 3 RGB bytes = 432 bytes = 864 hex characters
        elif len(line) == 864:
            try:
                data = ubinascii.unhexlify(line)
                summa=0
                for i in range(len(data)):
                    summa=summa+data[i]
                virta=summa*0.02/256 
                dimmer=3
                if virta>2: dimmer=int(virta)+3
                print('virta,dimmer',virta,dimmer)
                for zyy in range(144,144+72):
                     np[zyy]=(0,0,2)
                np[144+72-5]=(100,100,0)
                for i in range(LEDS):
                    r = data[i * 3] // dimmer
                    g = data[i * 3 + 1] // dimmer
                    b = data[i * 3 + 2] // dimmer
                    np[i] = (r, g, b)
                if flag>3 :
                    flag=0
                    np[144+71]=(255,0,0)
#                    np[146]=(255,0,0)
                flag = flag+1
                if dimmer>3:np[1]=(20,0,0)
                np.write()
                np2[0]=[0,0,0]
                np2.write()
            except Exception:
                print('erhe')
                pass

