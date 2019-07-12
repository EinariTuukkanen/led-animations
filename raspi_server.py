import time
import json
import socket
import threading

import neopixel
import board

import config as cfg

pixels = neopixel.NeoPixel(
    board.D18, cfg.TOTAL_LED_COUNT, auto_write=False, bpp=4)


def update_loop(pixels):
    while True:
        pixels.show()
        time.sleep(0.005)


if __name__ == '__main__':
    sock = socket.socket(
        socket.AF_INET,     # Internet
        socket.SOCK_DGRAM   # UDP
    )
    sock.bind((cfg.UDP_IP, cfg.UDP_PORT))

    last_update = time.time()
    # t = threading.Thread(target=update_loop, args=(pixels, ))
    # t.start()

    while True:
        raw_data, addr = sock.recvfrom(2**14)  # TODO: decide good buffer size
        data = json.loads(raw_data.decode('utf-8'))
        area = cfg.AREAS[data['area']]
        colors = data['colors']
        m = area.led_count // len(colors)
        colors2 = []
        for c in colors:
            colors2 += [c] * m
        area.update_colors(pixels, colors2)
        should_update = time.time()
        print(colors[10])
        if should_update - last_update >= 0.05:
            last_update = should_update
            pixels.show()
