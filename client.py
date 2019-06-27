import json
import socket

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

sock.sendto(encode_data(data), (cfg.UDP_IP, cfg.UDP_PORT))
