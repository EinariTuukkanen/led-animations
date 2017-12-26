import time
import random
import threading

from neopixel import *

import argparse
import signal
import sys


def signal_handler(signal, frame):
        colorWipe(strip, Color(0, 0, 0), 5)
        sys.exit(0)


def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-c',
            action='store_true',
            help='clear the display on exit'
        )
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT = 100  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN = 10  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def colorBeam(strip, color, wait_ms=20):
    """Shoots color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        if i > 0:
            strip.setPixelColor(i - 1, 0)
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(
                i,
                wheel((int(i * 256 / strip.numPixels()) + j) & 255)
            )
        strip.show()
        time.sleep(wait_ms/1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def randomFlash(strip, color, wait_ms=50):
    for i in range(0, strip.numPixels()):
        if not random.randint(0, 4):
            strip.setPixelColor(i, wheel(random.randint(0, 255)))
        else:
            strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms/1000.0)


def randomFlashBig(strip, color, wait_ms=100):
    for i in range(0, strip.numPixels(), 4):
        if not random.randint(0, 4):
            c = wheel(random.randint(0, 255))
            for j in range(4):
                strip.setPixelColor(i+j, c)
        else:
            for j in range(4):
                strip.setPixelColor(i+j, color)
    strip.show()
    time.sleep(wait_ms/1000.0)


def beam(strip, color, wait_ms=50, start=0, end=0, reverse=False, track=False):
    """Wipe color across display a pixel at a time."""
    end = end if end > start else strip.numPixels()
    rng = range(start, end)
    if reverse:
        rng = reversed(rng)
    for i in rng:
        if not track and i > 0:
            strip.setPixelColor(i - 1, 0)
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def police(strip, color1, color2, wait_ms=50):
    half = int(strip.numPixels() / 2)
    for i in range(0, half):
        strip.setPixelColor(i, color1)
    for i in range(half, strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
    time.sleep(wait_ms/1000.0)
    for i in range(0, half):
        strip.setPixelColor(i, 0)
    for i in range(half, strip.numPixels()):
        strip.setPixelColor(i, color2)
    strip.show()
    time.sleep(wait_ms/1000.0)


def fib(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

# fibs = []
# for i in range(0, 30):
#     fibs = fibs + [fib(i)]

def osku(strip, iterations=1, wait_ms=50):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    num = strip.numPixels()
    for i in range(256*iterations):
        j = 0
        n = 0
        #s = [0]*num
        while n < num:
            for k in range(0, fibs[j]):
                strip.setPixelColor(
                    (n + i) % strip.numPixels(),
                    Color(255, 255, 255)
                )
                #s[(n + i) % 200] = "0"
                n += 1
            j += 1
            #s[(n + i) % 200] = "1"
            strip.setPixelColor(
                    (n + i) % strip.numPixels(),
                    wheel((int(n * 256 / strip.numPixels()) + i) & 255)
                )
            n += 1
        #print(''.join(s))

        strip.show()
        time.sleep(wait_ms/1000.0)


def strobo(strip, color, wait_ms=50):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms/1000.0)
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
    time.sleep(wait_ms/1000.0)


def fade_in(strip, color, wait_ms=10):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, color)
    for a in range(0, 255, 5):
        strip.setBrightness(a)
        strip.show()
        time.sleep(wait_ms/1000.0)


def fade(strip, color, wait_ms=10):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, color)
    for a in range(0, 255, 5):
        strip.setBrightness(a)
        strip.show()
        time.sleep(wait_ms/1000.0)
    for a in reversed(range(0, 255, 5)):
        strip.setBrightness(a)
        strip.show()
        time.sleep(wait_ms/1000.0)
    strip.setBrightness(LED_BRIGHTNESS)


def center_beam(strip, color, wait_ms=20, track=False):
    half = int(strip.numPixels()/2)
    prevl = -1
    prevr = 1
    for i in range(0, half):
        if prevr >= 0 and not track:
            strip.setPixelColor(prevr, 0)
        prevr = half + i
        strip.setPixelColor(half + i, color)
        if prevl >= 0 and not track:
            strip.setPixelColor(prpyevl, 0)
        prevl = half - i
        strip.setPixelColor(half - i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
        LED_STRIP
    )
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    while True:
        # osku(strip)
        for i in range(0, 255, 50):
            center_beam(strip, wheel(i), 5, True)
        for i in range(0, 255, 50):
            fade(strip, wheel(i))
        for i in range(0, 50):
            strobo(strip, Color(255, 255, 255))
        for i in range(0, 50):
            police(strip, Color(255, 0, 0), Color(0, 255, 0))
        for i in range(0, 100):
            randomFlashBig(strip, 0)
        for i in range(0, 100):
            randomFlash(strip, 0)
        colorWipe(strip, Color(255, 0, 0))  # Red wipe
        colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        colorWipe(strip, Color(0, 0, 255))  # Green wipe
        theaterChase(strip, Color(127, 127, 127))  # White theater chase
        theaterChase(strip, Color(127,   0,   0))  # Red theater chase
        theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
        rainbow(strip)
        rainbowCycle(strip)
        theaterChaseRainbow(strip)
