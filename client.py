import json
import time
import socket
import colorsys

import config as cfg


def encode_data(data):
    return json.dumps(data).encode()


sock = socket.socket(
    socket.AF_INET,     # Internet
    socket.SOCK_DGRAM   # UDP
)

room = cfg.AREAS['olohuone']

data = {
    'areas': [room.name],
    'colors': [[255, 0, 0]] * room.led_count
}


def set_colors(areas, colors):
    data = {'areas': areas, 'colors': colors}
    sock.sendto(encode_data(data), (cfg.UDP_IP, cfg.UDP_PORT))


def rainbow():
    hue = 0
    while True:
        if hue > 1:
            hue = 0
        (r, g, b) = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        R, G, B = int(255 * r), int(255 * g), int(255 * b)
        set_colors([room.name], [[R, G, B]] * room.led_count)
        hue += 0.01
        time.sleep(0.01)


rainbow()
