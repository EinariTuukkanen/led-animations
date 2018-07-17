import json

from neopixel import ws, Adafruit_NeoPixel, Color
from flask import Flask, request

import config


class Strip(Adafruit_NeoPixel):
    """ Extends Adafruits NeoPixel by adding set all pixels at once -method """
    _prev_pixels = []

    def set_pixels(self, pixels):
        for i in range(len(pixels)):
            if (len(self._prev_pixels) == len(pixels) and
                    self._prev_pixels[i] == pixels[i]):
                continue
            self.setPixelColor(
                min(i + config.PIXEL_OFFSET, config.MAX_PIXEL_INDEX),
                pixels[i]
            )
        self.show()
        self._prev_pixels = pixels


def RGB(r=0, g=0, b=0):
    """ Converts strange RBG to more common RGB """
    return Color(r, b, g)


app = Flask(__name__)

# Connnect ws2811 LEDs
strip = Strip(
    config.MAX_PIXEL_INDEX,
    config.LED_PIN,
    config.LED_FREQ_HZ,
    config.LED_DMA,
    config.LED_INVERT,
    config.BRIGHTNESS,
    config.LED_CHANNEL,
    ws.WS2811_STRIP_GRB
)


@app.route('/color', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        raw_data = request.data
        if not raw_data:
            return 'No data'
        data = json.loads(str(raw_data.decode("utf-8")))
        strip.set_pixels([
            RGB(
                data.get('r', 0),
                data.get('g', 0),
                data.get('b', 0)
            ) for i in range(config.N_PIXELS)
        ])
        return 'Changed color: {}'.format(json.dumps(data))
    else:
        return 'Use POST to communicate'


strip.begin()
app.run(host='0.0.0.0', port=3000)