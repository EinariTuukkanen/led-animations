from pynput import keyboard
from neopixel import ws, Adafruit_NeoPixel, Color


class RGB(Color):
    def __init__(self, r=0, g=0, b=0):
        Color.__init__(self, r, b, g)


class Strip(Adafruit_NeoPixel):
    def single_color(self, color):
        for i in range(self.numPixels()):
            self.setPixelColor(i, color)
        self.show()

# LED strip configuration
LED_COUNT = 100  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering

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


def on_press(key):
    strip.single_color(RGB(255, 0, 0))


def on_release(key):
    strip.single_color(RGB())


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
