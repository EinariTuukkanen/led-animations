import socket
import json
from collections import namedtuple

from pynput import keyboard

from helper import error_msg, read_command


class Strip:
    def __init__(self, pixel_count, socket):
        self.pixel_count = pixel_count
        self.socket = socket

        self.pixels = [RGB(0, 0, 0) for i in range(self.pixel_count)]

    def set_pixel_color(self, index, color):
        self.pixels[index] = color

    def show(self):
        self.socket.send(json.dumps(self.pixels))

    def single_color(self, color):
        for i in range(self.pixel_count):
            self.set_pixel_color(i, color)
        self.show()


def on_press(key):
    if hasattr(key, 'char'):
        color = color_map.get(key.char, RGB(0, 0, 0))
        strip.single_color(color)


def on_release(key):
    strip.single_color(RGB(0, 0, 0))


ADDRESS = '192.168.10.44'
PORT = 8089
LED_COUNT = 100

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ADDRESS, PORT))

strip = Strip(LED_COUNT, clientsocket)

RGB = namedtuple('RGB', ['r', 'g', 'b'])

color_map = {
    'q': RGB(255, 0, 0),
    'w': RGB(0, 255, 0),
    'e': RGB(0, 0, 255),
}

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


while True:
    cmd, arg = read_command()

    if cmd == 'record':
        if not arg:
            error_msg('Not enough arguments')
            continue
        pass
    elif cmd == 'quit':
        break
    else:
        error_msg('Unknown command')

    # if not recording:
    #     raw = input('> ').split(' ')
    #     cmd = raw[0]

    #     # Handle escape char (\x1b = ESC)
    #     if '\x1b' in cmd:
    #         cmd = raw[0].split('\x1b')[-1]

    #     if cmd == 'record':
    #         if len(raw) == 2 and raw[1]:
    #             slot = raw[1]
    #             new_record = []
    #             print(
    #                 'Now recording to slot {}, '
    #                 'press esc to stop recording.'.format(slot))
    #             recording = True

    #     elif cmd == 'play':
    #         if len(raw) == 2 and raw[1]:
    #             slot = raw[1]
    #             print('Now playing from slot {}.'.format(slot))
    #             play_record(records[slot])

    #     elif cmd == 'quit':
    #         break

    #     else:
    #         print('Unknown command.')

listener.stop()
