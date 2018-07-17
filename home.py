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

colors = {
    'red': RGB(255, 0, 0),
    'green': RGB(0, 255, 0),
    'blue': RGB(0, 0, 255),
    'purple': RGB(255, 0, 255),
    'yellow': RGB(255, 255, 0),
    'turquoise': RGB(0, 255, 255),
    'white': RGB(255, 255, 255),
    'off': RGB(0, 0, 0)
}


@app.route('/color', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        raw_data = request.data
        if not raw_data:
            print('No data')
            return 'No data'
        data = json.loads(str(raw_data.decode("utf-8")))
        if 'color' in data and data['color'] in colors:
            color = colors[data['color']]
        elif 'r' in data and 'g' in data and 'b' in data:
            color = RGB(**data)
        else:
            print('Unknown data')
            return 'Unknown data'

        strip.set_pixels([color for i in range(config.N_PIXELS)])
        print('Changed color: {}'.format(json.dumps(data)))
        return 'Changed color: {}'.format(json.dumps(data))
    else:
        return 'Use POST to communicate'


strip.begin()
app.run(host='0.0.0.0', port=3000)
