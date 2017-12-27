from bluepy import btle


class BluetoothStrip(object):
    def __init__(self, address):
        self.address = address
        self.board = None
        self.char = None

    def connect_ble(self, address=''):
        self.board = btle.Peripheral(address or self.address)
        self.char = self._get_characteristic()

    def _get_characteristic(self):
        characteristics = self.board.getCharacteristics()
        return characteristics[7]

    def set_rgb(self, r, g, b):
        self._write([7, 5, 3, r, g, b])

    def set_brightness(self, a):
        self._write([4, 1, a, 255, 255, 255])

    def _write(self, params):
        self.char.write(self._format_data(params))

    def _format_data(self, params):
        if len(params) != 6:
            raise Exception
        return bytes(bytearray.fromhex(
            '7e{}00ef'.format(
                ''.join([format(p, 'x').zfill(2) for p in params])
            )
        ))
