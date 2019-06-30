import sys
import json
import socket
import config
import numpy as np
import colorsys

from helper import pack_msg

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.220', 8089))

j = 0

def _handle_stdin():
    global j
    while True:
        try:
            bar_heights = sys.stdin.readline().split(';')
            nums = list(map(int, bar_heights[:-2]))
            values = (np.array(nums)).astype(int) / 255
            hues = np.linspace(0, 1, 69)
            colors = (np.array([colorsys.hsv_to_rgb(hues[int(i + j) % 69], 1.0, values[i]) for i in range(69)]) * 255).astype(int).tolist()
            j += 0.1
            data = json.dumps(colors)
            clientsocket.sendall(pack_msg(data))

        except Exception as e:
            print(e)


if __name__ == '__main__':
    _handle_stdin()