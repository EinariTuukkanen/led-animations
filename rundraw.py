from threading import Thread
from time import sleep
from random import randint

from drawtest import VirtualLedStrip


def clamp(x):
    return max(0, min(x, 255))


def rgb_to_hex(r, g, b):
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))


strip = VirtualLedStrip(1000, 10, 100)


def updater(strip):
    colors = [rgb_to_hex(randint(0, 255), randint(0, 255), randint(0, 255))
              for i in range(strip.pixel_count)]
    strip.set_colors(colors)
    sleep(1)
    updater(strip)


thread = Thread(target=updater, args=(strip, ))
thread.start()

strip.run()
