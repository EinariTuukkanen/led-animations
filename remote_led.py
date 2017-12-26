import json
import socket

import numpy as np

import config
from helper import pack_msg


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((config.ADDRESS, config.PORT))


# Global variable for pixel state
pixels = np.tile(1, (3, config.N_PIXELS))


def update():
    # Limit and convert values
    _pixels = np.clip(pixels, 0, 255).astype(int)
    data = json.dumps(_pixels.tolist())
    clientsocket.sendall(pack_msg(data))
