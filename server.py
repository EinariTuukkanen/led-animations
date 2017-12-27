import socket
import json

from neopixel import ws, Adafruit_NeoPixel, Color
# from bluepy import btle

import config
from helper import recv_msg


# class BluetoothStrip(object):
#     def __init__(self, address):
#         self.address = address
#         self.board = None
#         self.char = None

#     def connect_ble(self, address=''):
#         self.board = btle.Peripheral(address or self.address)
#         self.char = self._get_characteristic()

#     def _get_characteristic(self):
#         characteristics = self.board.getCharacteristics()
#         return characteristics[7]

#     def set_rgb(self, r, g, b):
#         self._write([7, 5, 3, r, g, b])

#     def set_brightness(self, a):
#         self._write([4, 1, a, 255, 255, 255])

#     def _write(self, params):
#         self.char.write(self._format_data(params))

#     def _format_data(self, params):
#         if len(params) != 6:
#             raise Exception
#         return bytes(bytearray.fromhex(
#             '7e{}00ef'.format(
#                 ''.join([format(p, 'x').zfill(2) for p in params])
#             )
#         ))


class Strip(Adafruit_NeoPixel):
    """ Extends Adafruits NeoPixel by adding set all pixels at once -method """
    _prev_pixels = []

    def set_pixels(self, pixels):
        for i in range(len(pixels)):
            if (len(self._prev_pixels) == len(pixels) and
                    self._prev_pixels[i] == pixels[i]):
                continue
            self.setPixelColor(
                min(i + config.PIXEL_OFFSET, config.N_PIXELS),
                pixels[i]
            )
        self.show()
        self._prev_pixels = pixels


def buf_to_colors(buf):
    """ Extracts Color instances from json dump """
    try:
        colors = json.loads(buf)
    except Exception as e:
        print('Error while loading json {}'.format(e))
        return []

    ret = []
    for i in range(len(colors[0])):
        ret.append(Color(
            int(colors[0][i]),
            int(colors[2][i]),
            int(colors[1][i]))
        )
    return ret


# Init server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((config.ADDRESS, config.PORT))
serversocket.listen(config.MAX_CONNECTIONS)
connection, address = serversocket.accept()

# Connnect ws2811 LEDs
strip = Strip(
    100,
    config.LED_PIN,
    config.LED_FREQ_HZ,
    config.LED_DMA,
    config.LED_INVERT,
    config.BRIGHTNESS,
    config.LED_CHANNEL,
    ws.WS2811_STRIP_GRB
)
strip.begin()

# Connect bluetooth single color LEDs
# controller = BluetoothStrip(config.BLUETOOTH_ADDRESS)
# controller.connect_ble()


while True:
    buf = recv_msg(connection)
    if buf is not None:
        pixels = buf_to_colors(buf)
        strip.set_pixels(pixels)
    else:
        # Reconnect after a disconnect
        connection, address = serversocket.accept()
