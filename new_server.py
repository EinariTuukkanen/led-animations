import socket
import json
import struct
import time
from threading import Thread

from neopixel import ws, Adafruit_NeoPixel, Color

from helper import debug_msg


class Strip(Adafruit_NeoPixel):
    """ Extends Adafruits NeoPixel by adding set all pixels at once -method """
    _prev_pixels = []

    def set_pixels(self, colors):
        # p = np.copy(pixels)
        # # Encode 24-bit LED values in 32 bit integers
        # r = np.left_shift(p[0][:].astype(int), 8)
        # g = np.left_shift(p[1][:].astype(int), 16)
        # b = p[2][:].astype(int)
        # rgb = np.bitwise_or(np.bitwise_or(r, g), b)
        # # Update the pixels
        # for i in range(config.N_PIXELS):
        #     # Ignore pixels if they haven't changed (saves bandwidth)
        #     if np.array_equal(p[:, i], _prev_pixels[:, i]):
        #         continue
        #     strip._led_data[i] = rgb[i]
        # _prev_pixels = np.copy(p)
        # strip.show()

        for i in range(len(colors)):
            self.setPixelColor(i, colors[i])
        self.show()
        # self._prev_pixels = colors


def buf_to_colors(buf):
    """ Extracts Color instances from json dump """
    try:
        colors = json.loads(buf)
    except Exception as e:
        print('Error while loading json {}'.format(e))
        # print(buf)
        # time.sleep(10)
        return []

    ret = []
    for i in range(len(colors[0])):
        ret.append(Color(
            int(colors[0][i]),
            int(colors[2][i]),
            int(colors[1][i]))
        )
    return ret


# Server configuration
ADDRESS = '192.168.10.44'  # Address of the computer server is running on
PORT = 8089
MAX_CONNECTIONS = 5  # Number of allowed connections
DEBUG = False

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
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((ADDRESS, PORT))
serversocket.listen(MAX_CONNECTIONS)
connection, address = serversocket.accept()

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

db = []


def update_color(buf):
    global db
    colors = buf_to_colors(buf)
    # strip.set_pixels(colors)
    db.append(colors)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


while True:
    if len(db) > 1000:
        break
    # buf = connection.recv(7296)
    buf = recv_msg(connection)
    if len(buf) > 0:
        update_color(buf)
        # t = Thread(target=update_color, args=(buf,))
        # t.start()
    else:
        # Reconnect after a disconnect
        connection, address = serversocket.accept()

for i in range(len(db)):
    print('playing: ', i)
    strip.set_pixels(db[i])
    time.sleep(0.5)
