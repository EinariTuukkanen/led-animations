import neopixel
import board

import config as cfg

pixels = neopixel.NeoPixel(board.D18, cfg.TOTAL_LED_COUNT, auto_write=False)

room = cfg.AREAS['room']
colors = [(255, 0, 0)] * room.led_count

if __name__ == '__main__':
    room.update_colors(pixels, colors)
