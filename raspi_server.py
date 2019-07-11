import json
import socket

import neopixel

import config as cfg

pixels = neopixel.NeoPixel(cfg.GPIO_PIN, cfg.TOTAL_LED_COUNT, auto_write=False)


if __name__ == '__main__':
    sock = socket.socket(
        socket.AF_INET,     # Internet
        socket.SOCK_DGRAM   # UDP
    )
    sock.bind((cfg.UDP_IP, cfg.UDP_PORT))

    while True:
        raw_data, addr = sock.recvfrom(2**14)  # TODO: decide good buffer size
        data = json.loads(raw_data.decode('utf-8'))
        area = cfg.AREAS[data['area']]
        area.update_colors(pixels, data['colors'])
