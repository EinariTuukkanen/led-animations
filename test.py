from neopixel import ws, Adafruit_NeoPixel, Color

import config

strip = Adafruit_NeoPixel(
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
strip.setPixelColor(30, Color(255, 0, 0))
