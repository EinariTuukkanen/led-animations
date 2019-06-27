import json
import time
import socket
import random
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
    off = 0
    m = 100.0 / room.led_count
    while True:
        if off > 1:
            off = 0
        colors = []
        for i in range(room.led_count):
            (r, g, b) = colorsys.hsv_to_rgb(i * m / 100 + off, 1.0, 1.0)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            colors.append([R, G, B])
        set_colors([room.name], colors)
        off += 0.01
        time.sleep(0.01)


def ripple():
    off = 0
    m = 100.0 / room.led_count
    s = 0
    ss = 1
    maxs = random.randint(10, 1000)
    while True:
        if off > 1:
            off = 0
        if off < 0:
            off = 1
        if s > maxs:
            s = 0
            ss = -ss
            maxs = random.randint(10, 1000)
        colors = []
        for i in range(room.led_count):
            j = i % 10
            k = (1 - abs(round(j / 10) * 10 - j) / 10) ** 3
            (r, g, b) = colorsys.hsv_to_rgb(i * m / 100 + off, 1.0, k)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            colors.append([R, G, B])
        set_colors([room.name], colors)
        off += ss * 0.01
        time.sleep(0.01)
        s += 1


ripple()
