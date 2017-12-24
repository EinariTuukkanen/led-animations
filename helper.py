from collections import namedtuple
from enum import Enum

DEBUG = False

RGB = namedtuple('RGB', ['r', 'g', 'b'])


class InputMode(Enum):
    """ Different input modes """
    COMMAND = 1
    RECORD = 2
    FREE = 3


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
