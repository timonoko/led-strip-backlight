import machine, neopixel,time

np = neopixel.NeoPixel(machine.Pin(48), 1)

from camera import Camera, FrameSize, PixelFormat

cam = Camera(frame_size = 15,pixel_format=PixelFormat.JPEG,init=False)

cam.init()

for x in range(3):
    np[0]=[255,255,255]
    np.write()
    a=cam.capture()
    np[0]=[0,0,0]
    np.write()
    time.sleep(1)
    print(x,len(a))
    if x==2:
        f=open('kuva.jpg','w')
        f.write(a)
        f.close()
