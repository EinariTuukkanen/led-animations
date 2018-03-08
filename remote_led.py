import json
import socket

import numpy as np
from bluepy import btle

import config
from helper import pack_msg


class BluetoothStrip(object):
    def __init__(self, address):
        self.address = address
        self.board = None
        self.char = None

    def connect_ble(self, address=''):
        self.board = btle.Peripheral(address or self.address)
        self.char = self._get_characteristic()

    def _get_characteristic(self):
        characteristics = self.board.getCharacteristics()
        return characteristics[7]

    def set_rgb(self, r, g, b):
        self._write([7, 5, 3, r, g, b])

    def set_brightness(self, a):
        self._write([4, 1, a, 255, 255, 255])

    def _write(self, params):
        self.char.write(self._format_data(params))

    def _format_data(self, params):
        if len(params) != 6:
            raise Exception
        return bytes(bytearray.fromhex(
            '7e{}00ef'.format(
                ''.join([format(p, 'x').zfill(2) for p in params])
            )
        ))

if config.USE_RPI_LED:
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((config.ADDRESS, config.PORT))

# Connect bluetooth single color LEDs
if config.USE_BLUETOOTH_LED:
    strip = BluetoothStrip(config.BLUETOOTH_ADDRESS)
    strip.connect_ble()

# Global variable for pixel state
pixels = np.tile(1, (3, config.N_PIXELS))


def avg(arr):
    return int(sum(arr) / len(arr))


def update():
    # Limit and convert values
    _pixels = np.clip(pixels, 0, 255).astype(int).tolist()
    if config.USE_BLUETOOTH_LED:
        strip.set_rgb(avg(_pixels[0]), avg(_pixels[1]), avg(_pixels[2]))
    if config.USE_RPI_LED:
        data = json.dumps(_pixels)
        clientsocket.sendall(pack_msg(data))
