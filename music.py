#!/usr/bin/python3
import argparse
import math
import socket
import json

import numpy as np
import sounddevice as sd

import config as cfg

sock = socket.socket(
    socket.AF_INET,     # Internet
    socket.SOCK_DGRAM   # UDP
)

room = cfg.AREAS['room']


def update_colors(area, colors):
    data = {'area': area.name, 'colors': colors}
    sock.sendto(json.dumps(data).encode(), (cfg.UDP_IP, cfg.UDP_PORT))


def rainbow(pos):
    """Applies rainbow colouring on pixels red->blue->green->red(orange)"""
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    elif pos < 170:
        pos -= 85
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    else:
        pos -= 170
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    return (r, g, b)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def main(parser, room):
    try:
        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)

        samplerate = sd.query_devices(args.device, 'input')[
            'default_samplerate']

        delta_f = (high - low) / (room.led_count - 1)
        fftsize = math.ceil(samplerate / delta_f)
        # low_bin = math.floor(low / delta_f)

        # For smoothing, we keep our previous values
        previous_values = [0] * room.led_count
        smoothing = args.smoothing ** (1 / 8)

        def audio_callback(indata, frames, time, status):
            if any(indata):
                # Do Fast Fourier Transform on the audio data
                magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
                magnitude *= args.gain / fftsize

                # Take only the frequencies we're interested in
                grouped = [[] for i in range(room.led_count)]
                for i, x in enumerate(
                        magnitude[int(low // delta_f):int(high // delta_f)]):
                    grouped[int(i)].append(x)

                # This scales the actual freqency magnitudes so that lower
                # magnitudes get picked up better, especially on higher freqs
                # where magnitudes are lower despite sounding as powerful as
                # the lower ones, due to logarithmic perception of sound in
                # humans. I suck at DSP, so take with a grain of salt.
                for i, x in enumerate(grouped):
                    if len(x) > 0 and np.max(x) > 0:
                        grouped[i] = ((i + 1) / room.led_count) * \
                            args.gain * abs(np.max(x)) ** 2
                    else:
                        grouped[i] = 0

                colors = []
                # Thanks to batching our operations, we'll append every
                # LED's update call into a single packet
                for i, x in enumerate(grouped):
                    previous = previous_values[i]
                    value = np.clip(x, 1 / 255, 1)

                    #  Smooth the value
                    if value < previous:
                        value = previous * smoothing + x * (1 - smoothing)
                    br = value
                    previous_values[i] = value

                    # Calculate pixel color on an 256 segment rainbow
                    pos = (i * 256 // room.led_count)
                    r, g, b = rainbow(pos & 255)

                    # Apply brightness (magnitude from FFT)
                    r = math.ceil(r * br)
                    g = math.ceil(g * br)
                    b = math.ceil(b * br)

                    colors.append([r, g, b])
                update_colors(room, colors)

        with sd.InputStream(
                device=args.device, channels=1,
                callback=audio_callback,
                blocksize=int(samplerate * args.block_duration / 1000),
                samplerate=samplerate):
            print('Successfully started InputStream')
            while True:
                response = input()
                if response in ('', 'q', 'Q'):
                    break

    except KeyboardInterrupt:
        parser.exit('Stopped')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


# Arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-l', '--list-devices', action='store_true',
                    help='list audio devices and exit')
parser.add_argument('-b', '--block-duration', type=float,
                    metavar='DURATION', default=50,
                    help='block size (default %(default)s milliseconds)')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='input device (numeric ID or substring)')
parser.add_argument('-g', '--gain', type=float, default=10,
                    help='initial gain factor (default %(default)s)')
parser.add_argument('-r', '--range', type=float, nargs=2,
                    metavar=('LOW', 'HIGH'), default=[20, 2500],
                    help='frequency range (default %(default)s Hz)')
parser.add_argument('-s', '--smoothing', type=float, default=0.2,
                    help='smoothing factor (default %(default)s)')

args = parser.parse_args()

low, high = args.range
if high <= low:
    parser.error('HIGH must be greater than LOW')

if __name__ == '__main__':
    main(parser, room)
