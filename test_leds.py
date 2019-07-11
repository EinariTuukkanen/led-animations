import neopixel
import board

import config as cfg


room = cfg.AREAS['olohuone']
strip = neopixel.NeoPixel(board.D12, room.led_count, auto_write=False)

strip.fill((255, 0, 0,))
