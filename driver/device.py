from machine import Pin, UART


class Device:
    """
    Class created for accessing connected sub devices.
    """
    def __init__(self, neopixels,
                 ir_receiver,
                 led: Pin,
                 uart: UART):
        self._neopixels = neopixels
        self._ir_receiver = ir_receiver
        self._led = led
        self._uart = uart

    @property
    def neopixels(self):
        return self._neopixels

    @property
    def ir_receiver(self):
        return self._ir_receiver

    @property
    def led(self):
        return self._led

    @property
    def uart(self):
        return self._uart