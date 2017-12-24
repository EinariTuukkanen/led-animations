import socket
import json

from pynput import keyboard

from helper import error_msg, read_command, RGB, InputMode


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
    if mode != InputMode.COMMAND:
        if hasattr(key, 'char'):
            color = color_map.get(key.char, RGB(0, 0, 0))
            strip.single_color(color)


def on_release(key):
    if mode != InputMode.COMMAND:
        strip.single_color(RGB(0, 0, 0))


ADDRESS = '192.168.10.44'
PORT = 8089
LED_COUNT = 100

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ADDRESS, PORT))

strip = Strip(LED_COUNT, clientsocket)

color_map = {
    'q': RGB(255, 0, 0),
    'w': RGB(0, 255, 0),
    'e': RGB(0, 0, 255),
}

mode = InputMode.COMMAND

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    while True:
        cmd, arg = read_command()

        if cmd == 'record':
            if not arg:
                error_msg('Not enough arguments')
                continue
            mode = InputMode.RECORD

        elif cmd == 'quit':
            break

        else:
            error_msg('Unknown command')
            continue
