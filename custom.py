import sys
import requests
import json
import struct
from scipy.stats import norm
import numpy as np

def _get_spaced_colors(n):
    max_value = 16581375
    interval = int(max_value / n)
    colors = [hex(i)[2:].zfill(6) for i in range(0, max_value, interval)]

    return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]


ALL_COLORS = _get_spaced_colors(100)


# def _handle_stdin():
#     while True:
#         try:
#             nums = map(int, sys.stdin.readline()[:-2].split(';'))
#             colors = [ALL_COLORS[num] for num in nums]
#             print(colors)
#             r = requests.post('http://192.168.1.220:3000/cava', json={'colors': colors})

#         except Exception as e:
#             print(e)

import socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.220', 8089))
LEDCOUNT = 69


def pack_msg(data):
    return struct.pack('>I', len(data)) + str.encode(data)


def _handle_stdin():
    while True:
        try:
            nums = list(map(int, sys.stdin.readline()[:-2].split(';')))
            colors = np.array([
                np.array(ALL_COLORS[i]) * (n / 255) for i, n in enumerate(nums)
            ])
            print(colors)
            dx = 3 / 34
            m = 2.5
            dist = np.array([m * norm.pdf(0 + dx * (i - 34)) for i in range(69)])
            balanced_colors = [colors * x for x in dist]
            
            r = []
            g = []
            b = []
            for xcolors in balanced_colors:
                r.append(max([c[0] for c in xcolors]))
                g.append(max([c[1] for c in xcolors]))
                b.append(max([c[2] for c in xcolors]))


            # relative_colors = nums / 255
            # c = [ALL_COLORS[num] for num in nums]
            # r = [a[0] for a in c]
            # g = [a[1] for a in c]
            # b = [a[2] for a in c]
            # g = [0] * 69
            # b = [0] * 69
            colors = [r, g, b]
            data = json.dumps(colors)
            clientsocket.sendall(pack_msg(data))

        except Exception as e:
            print(e)


if __name__ == '__main__':
    _handle_stdin()