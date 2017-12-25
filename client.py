import socket
import threading

from pynput import keyboard

from helper import error_msg, read_command, RGB, InputMode, Record, Effect
from ledstrip import Strip


def on_press(key):
    global mode, record, records
    if mode != InputMode.COMMAND:
        if hasattr(key, 'char'):
            # Alphanumeric key
            effect = effect_map.get(key.char, RGB(0, 0, 0))
            t = threading.Thread(target=effect.callback, args=effect.args)
            t.start()

            if mode == InputMode.RECORD:
                record.append(key.char, kb_controller.press)
        else:
            # Special key
            if key == key.esc:
                if mode == InputMode.RECORD:
                    records[record.name] = record
                mode = InputMode.COMMAND
            if key == key.caps_lock:
                strip.blend = True
                print('Blend on')


def on_release(key):
    global mode, record

    if mode != InputMode.COMMAND:
        strip.single_color(RGB(0, 0, 0))
        if hasattr(key, 'char'):
            if mode == InputMode.RECORD:
                record.append(key.char, kb_controller.release)

        elif key == key.caps_lock:
            strip.blend = False
            print('Blend off')


ADDRESS = '192.168.10.44'
PORT = 8089
LED_COUNT = 100

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ADDRESS, PORT))

kb_controller = keyboard.Controller()

strip = Strip(LED_COUNT, clientsocket)

mode = InputMode.COMMAND

records = {}
record = []

effect_map = {
    'q': Effect(strip.single_color, [RGB(255, 0, 0)]),
    'w': Effect(strip.single_color, [RGB(0, 255, 0)]),
    'e': Effect(strip.single_color, [RGB(0, 0, 255)]),
    'r': Effect(strip.center_shockwave, [RGB(255, 0, 0), 1]),
    't': Effect(strip.center_shockwave, [RGB(0, 255, 0), 2]),
    'y': Effect(strip.center_shockwave, [RGB(0, 0, 255), 3]),
}


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    while True:
        if mode != InputMode.COMMAND:
            continue

        cmd, arg = read_command()

        if cmd == 'record':
            if not arg:
                error_msg('Not enough arguments')
                continue
            mode = InputMode.RECORD
            record = Record(arg)

        elif cmd == 'free':
            mode = InputMode.FREE

        elif cmd == 'play':
            if not arg:
                error_msg('Not enough arguments')
                continue
            r = records.get(arg, None)
            if r:
                mode = InputMode.PLAYBACK
                r.play()
                mode = InputMode.COMMAND

        elif cmd == 'quit':
            break

        elif cmd == '':
            continue

        else:
            error_msg('Unknown command')
            continue
