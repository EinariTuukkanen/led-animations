import json

from helper import RGB, wait


class Strip:
    def __init__(self, pixel_count, socket):
        self.pixel_count = pixel_count
        self.socket = socket

        self.blend = False
        self.pixels = [RGB(0, 0, 0) for i in range(self.pixel_count)]

    def set_pixel_color(self, index, color):
        # if self.blend:
            # color = self.pixels[index] + color
        self.pixels[index] = color

    def show(self):
        self.socket.send(json.dumps(self.pixels))

    def single_color(self, color):
        for i in range(self.pixel_count):
            self.set_pixel_color(i, color)
        self.show()

    def center_shockwave(self, color, length=1, wait_ms=10):
        center = int(self.pixel_count / 2)
        for i in range(0, center):
            self.set_pixel_color(i + center, color)  # Up
            self.set_pixel_color(center - i, color)  # Down
            if i > length:
                j = i - length
                self.set_pixel_color(j + center, RGB(0, 0, 0))  # Up
                self.set_pixel_color(center - j, RGB(0, 0, 0))  # Down
            self.show()
            wait(wait_ms)
        for i in range(center - length, center):
            self.set_pixel_color(i + center, RGB(0, 0, 0))  # Up
            self.set_pixel_color(center - i, RGB(0, 0, 0))  # Down
        self.show()
