import socket
import json

import numpy as np
from neopixel import ws, Adafruit_NeoPixel, Color

from helper import recv_msg
import config

_gamma = np.load(config.GAMMA_TABLE_PATH)


class Strip(Adafruit_NeoPixel):
    """ Extends Adafruits NeoPixel by adding set all pixels at once -method """
    _prev_pixels = []

    def set_pixels(self, pixels):
        p = _gamma[pixels] if config.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)
        # Encode 24-bit LED values in 32 bit integers
        r = np.left_shift(p[0][:].astype(int), 8)
        g = np.left_shift(p[1][:].astype(int), 16)
        b = p[2][:].astype(int)
        rgb = np.bitwise_or(np.bitwise_or(r, g), b)
        # Update the pixels
        for i in range(config.N_PIXELS):
            # Ignore pixels if they haven't changed (saves bandwidth)
            if np.array_equal(p[:, i], self._prev_pixels[:, i]):
                continue
            strip._led_data[i] = rgb[i]
        self._prev_pixels = np.copy(p)

        # for i in range(len(colors)):
        #     self.setPixelColor(i, colors[i])
        # self.show()
        # self._prev_pixels = colors


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


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((config.ADDRESS, config.PORT))
serversocket.listen(config.MAX_CONNECTIONS)
connection, address = serversocket.accept()

strip = Strip(
    config.N_PIXELS,
    config.LED_PIN,
    config.LED_FREQ_HZ,
    config.LED_DMA,
    config.LED_INVERT,
    config.BRIGHTNESS,
    config.LED_CHANNEL,
    ws.WS2811_STRIP_GRB
)
strip.begin()


while True:
    buf = recv_msg(connection)
    if len(buf) > 0:
        # pixels = buf_to_colors(buf)
        try:
            pixels = json.loads(buf)
        except Exception as e:
            print('Error while loading json {}'.format(e))
            continue
        strip.set_pixels(pixels)
    else:
        # Reconnect after a disconnect
        connection, address = serversocket.accept()
