import json
import socket

from neopixel import ws, Adafruit_NeoPixel, Color

import config as cfg


class LedStrip(Adafruit_NeoPixel):
    def __init__(self, area, pin, freq_hz=800000, dma=10,
                 invert=False, brightness=255, channel=0,
                 strip_type=ws.WS2811_STRIP_RGB):
        self.area = area
        super().__init__(
            self.area.led_count, pin, freq_hz, dma, invert,
            brightness, channel, strip_type
        )
        self.state = []
        try:
            self.begin()
        except RuntimeError as e:
            print('Error', e)
            exit('Did you run with root privileges?')

    def set_pixel_colors(self, colors=[]):
        # Reset colors with empty method call
        if not colors:
            colors = [Color(0, 0, 0)] * self.area.led_count

        if len(colors) != self.area.led_count:
            raise Exception(
                'Got {n} colors for {m} pixels'.format(
                    n=len(colors), m=self.area.led_count
                )
            )

        for i, color in enumerate(colors):
            # TODO: skip update if state not changed
            self.setPixelColor(self.area.start_index + colors[i], color)

        self.show()
        self.state = colors

    def set_pixel_colors_rgb(self, colors_rgb=[]):
        self.set_pixel_colors([Color(r, g, b) for (r, g, b) in colors_rgb])


class LedSystem:
    def __init__(self, area_strips={}):
        self.area_strips = area_strips

    def set_area_colors(self, colors=[], areas=[]):
        # Without specified area, run for all areas
        if not areas:
            areas = self.area_strips.keys()

        for name in areas:
            if name not in self.area_strips:
                raise Exception('Invalid area {name}'.format(name=name))
            self.area_strips[name].set_pixel_colors(colors)

    def set_area_colors_rgb(self, colors_rgb=[], areas=[]):
        self.set_area_colors(
            [Color(r, g, b) for (r, g, b) in colors_rgb], areas
        )


if __name__ == '__main__':
    UDP_IP = cfg.UDP_IP
    UDP_PORT = cfg.UDP_PORT

    sock = socket.socket(
        socket.AF_INET,     # Internet
        socket.SOCK_DGRAM   # UDP
    )
    sock.bind((UDP_IP, UDP_PORT))

    common_configs = [
        cfg.LED_PIN,
        cfg.LED_FREQ_HZ,
        cfg.LED_DMA,
        cfg.LED_INVERT,
        cfg.BRIGHTNESS,
        cfg.LED_CHANNEL,
        ws.WS2811_STRIP_RGB
    ]

    # Connnect ws2811 LEDs into one system
    system = LedSystem({
        area.name: LedStrip(area, *common_configs)
        for area in cfg.AREAS.values()
    })

    while True:
        data, addr = sock.recvfrom(2**14)  # buffer size is 1024 bytes
        data = json.loads(data.decode('utf-8'))
        print('received message:', data)
        system.set_area_colors_rgb(data['colors'], data['areas'])
