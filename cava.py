import sys
import requests
import json
import struct
import numpy as np
import dsp
import config
from scipy.ndimage.filters import gaussian_filter1d

def _get_spaced_colors(n):
    max_value = 16581375
    interval = int(max_value / n)
    colors = [hex(i)[2:].zfill(6) for i in range(0, max_value, interval)]

    return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]


ALL_COLORS = _get_spaced_colors(256)


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

# samples_per_frame = int(config.MIC_RATE / config.FPS)
y_roll = np.random.rand(config.N_ROLLING_HISTORY, 100) / 1e16

fft_window = np.hamming(100 * config.N_ROLLING_HISTORY)
mel_gain = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.01, alpha_rise=0.99)
mel_smoothing = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.5, alpha_rise=0.99)

p = np.tile(1.0, (3, config.N_PIXELS // 2))
gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                     alpha_decay=0.001, alpha_rise=0.99)

def pack_msg(data):
    return struct.pack('>I', len(data)) + str.encode(data)



def visualize_energy(y):
    """Effect that expands from the center with increasing sound energy"""
    global p
    y = np.copy(y)
    gain.update(y)
    y /= gain.value
    # Scale by the width of the LED strip
    y *= float((config.N_PIXELS // 2) - 1)
    # Map color channels according to energy in the different freq bands
    scale = 0.9
    r = int(np.mean(y[:len(y) // 3]**scale))
    g = int(np.mean(y[len(y) // 3: 2 * len(y) // 3]**scale))
    b = int(np.mean(y[2 * len(y) // 3:]**scale))
    # Assign color to different frequency regions
    p[0, :r] = 255.0
    p[0, r:] = 0.0
    p[1, :g] = 255.0
    p[1, g:] = 0.0
    p[2, :b] = 255.0
    p[2, b:] = 0.0
    p_filt.update(p)
    p = np.round(p_filt.value)
    # Apply substantial blur to smooth the edges
    p[0, :] = gaussian_filter1d(p[0, :], sigma=4.0)
    p[1, :] = gaussian_filter1d(p[1, :], sigma=4.0)
    p[2, :] = gaussian_filter1d(p[2, :], sigma=4.0)
    # Set the new pixel value
    return np.concatenate((p[:, ::-1], p), axis=1)


def _handle_stdin():
    while True:
        try:
            nums = np.array(list(map(int, sys.stdin.readline()[:-2].split(';'))))
            y = nums / 255
            # Construct a rolling window of audio samples
            y_roll[:-1] = y_roll[1:]
            y_roll[-1, :] = np.copy(y)
            y_data = np.concatenate(y_roll, axis=0).astype(np.float32)



            # Transform audio input into the frequency domain
            N = len(y_data)
            N_zeros = 2**int(np.ceil(np.log2(N))) - N
            # Pad with zeros until the next power of two
            y_data *= fft_window
            y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
            YS = np.abs(np.fft.rfft(y_padded)[:N // 2])

            # Construct a Mel filterbank from the FFT data
            asdasd = dsp.mel_y.T
            mel = np.atleast_2d(YS).T * asdasd

            # Scale data to values more suitable for visualization
            # mel = np.sum(mel, axis=0)
            mel = np.sum(mel, axis=0)
            mel = mel**2.0

            # Gain normalization
            mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))

            mel /= mel_gain.value
            mel = mel_smoothing.update(mel)

            # Map filterbank output onto LED strip
            output = visualize_energy(y)
            
            # r = [a[0] for a in c]
            # g = [a[1] for a in c]
            # b = [a[2] for a in c]
            # colors = [r, g, b]
            print(output)
            # data = json.dumps(colors)
            # clientsocket.sendall(pack_msg(data))

        except Exception as e:
            print(e)


if __name__ == '__main__':
    _handle_stdin()