from collections import namedtuple
from enum import Enum
from time import time, sleep


DEBUG = False

KeyEvent = namedtuple('KeyEvent', ['value', 'callback', 'timestamp'])
# RGB = namedtuple('RGB', ['r', 'g', 'b'])
Effect = namedtuple('Effect', ['callback', 'args'])


class RGB(list):
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b
        self.append(r)
        self.append(g)
        self.append(b)

    def __add__(self, o):
        return RGB(
            min(self.r + o.r, 255),
            min(self.g + o.g, 255),
            min(self.b + o.b, 255),
        )


class Record(list):
    """ Single record that stores pressed key events """
    def __init__(self, name):
        self.name = name
        self.events = []
        self.timedelta = 0

    def append(self, value, callback):
        timestamp = time()
        if not self.timedelta:
            self.timedelta = timestamp
        tmp = timestamp
        timestamp = timestamp - self.timedelta
        self.timedelta = tmp
        list.append(self, KeyEvent(value, callback, timestamp))

    def play(self):
        for key in self:
            sleep(key.timestamp)
            key.callback(key.value)


class InputMode(Enum):
    """ Different input modes """
    COMMAND = 1
    RECORD = 2
    FREE = 3
    PLAYBACK = 4


def debug_msg(msg):
    """ Debug message """
    if DEBUG:
        print('[DEBUG] {}'.format(msg))


def error_msg(msg):
    """ Error message """
    print('[ERROR] {}'.format(msg))


def read_command():
    raw = raw_input('> ').split(' ')
    cmd = raw[0]

    # Handle escape char (\x1b = ESC)
    if '\x1b' in cmd:
        cmd = raw[0].split('\x1b')[-1]

    if len(raw) >= 2 and raw[1]:
        return cmd, raw[1]

    return cmd, None


def wait(ms):
    sleep(ms / 1000.0)
