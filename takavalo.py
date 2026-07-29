#!/usr/bin/env python3
import os
import time
import serial
from PIL import Image

PORT = '/dev/ttyACM0'  # Serial port connected to ESP32
BAUD = 115200

ser = serial.Serial(PORT, BAUD)
print(f"Connected to {PORT}. Streaming hex backlight colors...")

try:
    while True:
        os.system('scrot kuva.jpg')
        im = Image.open('kuva.jpg')
        W, H = im.size
        suhde = W / 144

        raw_bytes = bytearray()
        for y in range(144):
            z = 143 - y
            px = min(int(z * suhde), W - 1)
            r, g, b = im.getpixel((px, 100))[:3]
            raw_bytes.extend([r, g, b])

        # Convert raw bytes to hex string + newline (safe from Ctrl+C / Ctrl+D)
        hex_line = raw_bytes.hex() + '\n'
        ser.write(hex_line.encode('ascii'))
        time.sleep(0.03)  # ~30 FPS
except KeyboardInterrupt:
    print("\nStopped streaming.")
finally:
    try:
        ser.write(b'STOP\n')
        ser.flush()
    except Exception:
        pass
    ser.close()

