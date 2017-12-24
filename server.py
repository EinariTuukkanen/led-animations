import socket
import json

from neopixel import ws, Adafruit_NeoPixel, Color


class Strip(Adafruit_NeoPixel):
    def set_pixels(self, colors):
        for i in range(self.numPixels()):
            self.setPixelColor(i, colors[i])
        self.show()

    def single_color(self, color):
        for i in range(self.numPixels()):
            self.setPixelColor(i, color)
        self.show()


def buf_to_colors(buf):
    try:
        colors = json.loads(buf)
    except Exception as e:
        print('Error while loading json', e)

    for i in range(len(colors)):
        colors[i] = Color(colors[i][0], colors[i][2], colors[i][1])
    print(colors)
    return colors


# Server configuration
ADDRESS = '192.168.10.44'  # Address of the computer server is running on
PORT = 8089
MAX_CONNECTIONS = 5  # Number of allowed connections

# LED strip configuration
LED_COUNT = 100  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((ADDRESS, PORT))
serversocket.listen(MAX_CONNECTIONS)

strip = Strip(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
    LED_STRIP
)
strip.begin()


while True:
    connection, address = serversocket.accept()
    buf = connection.recv(4096)
    if len(buf) > 0:
        strip.set_pixels(buf_to_colors(buf))
