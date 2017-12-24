import socket
import json
from collections import namedtuple

from pynput import keyboard


ADDRESS = '192.168.10.44'  # Address of the computer server is running on
PORT = 8089

LED_COUNT = 100  # Number of LED pixels.

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ADDRESS, PORT))

RGB = namedtuple('RGB', ['r', 'g', 'b'])


class Strip:
    def __init__(self, pixel_count, socket):
        self.pixel_count = pixel_count
        self.socket = socket

        self.pixels = [RGB(0, 0, 0) for i in range(self.pixel_count)]

    def single_color(self, color):
        for i in range(self.pixel_count):
            self.set_pixel_color(i, color)
        self.show()

    def set_pixel_color(self, index, color):
        self.pixels[index] = color

    def show(self):
        self.socket.send(json.dumps(self.pixels))


def on_press(key):
    strip.single_color(RGB(255, 0, 0))


def on_release(key):
    strip.single_color(RGB(0, 0, 0))


strip = Strip(LED_COUNT, clientsocket)

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
