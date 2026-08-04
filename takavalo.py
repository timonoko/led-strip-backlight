#!/usr/bin/env python3
import os
import time
import serial
from PIL import Image



PORT = '/dev/ttyACM0'  # Serial port connected to ESP32
BAUD = 115200

print(f"Connected to {PORT}. Streaming hex backlight colors...")


laskuri=0
try:
    while True:
        if laskuri==0:
            os.system('mpremote a0 exec --no-follow "import taka"')
            ser = serial.Serial(PORT, BAUD)
        laskuri+=1
        print(laskuri)
        if laskuri>10000:
            laskuri=0
            ser.write(b'STOP\n')
        print('scrot')
        os.system('scrot kuva.jpg')
        im = Image.open('kuva.jpg')
        W, H = im.size
        suhde = W / 144
        if W<2000:line=200
        else: line=1000    

        raw_bytes = bytearray()
        for y in range(144):
            z = 143 - y
            px = min(int(z * suhde), W - 1)
            r, g, b = im.getpixel((px, line))[:3]
            raw_bytes.extend([r, g, b])

        # Convert raw bytes to hex string + newline (safe from Ctrl+C / Ctrl+D)
        hex_line = raw_bytes.hex() + '\n'
        print('serwrite')
        ser = serial.Serial(PORT, BAUD)
        ser.write(hex_line.encode('ascii'))
        print(W)
        time.sleep(0.2)  # ~30 FPS
except KeyboardInterrupt:
    print("\nStopped streaming.")
finally:
    try:
        ser.write(b'STOP\n')
        ser.flush()
    except Exception:
        pass
    ser.close()
    os.system('mpremote a0 reset')
