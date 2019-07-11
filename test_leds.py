import neopixel

import config as cfg


room = cfg.AREAS['olohuone']
strip = neopixel.NeoPixel(cfg.LED_PIN, room.led_count, auto_write=False)

strip.fill((255, 0, 0,))
