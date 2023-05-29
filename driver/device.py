from neopixel import NeoPixel


class Device:
    """
    Class created for accessing connected sub devices.
    """
    def __init__(self, neopixels: NeoPixel,
                 np_groups: [],
                 ir_receiver):
        self._neopixels = neopixels
        self._np_groups = np_groups
        self._ir_receiver = ir_receiver

    @property
    def strip(self):
        return self._neopixels

    @property
    def np_groups(self):
        return self._np_groups

    def get_np_group(self, i):
        return self._np_groups[i]

    @property
    def ir_receiver(self):
        return self._ir_receiver

