

class Device:
    """
    Class created for accessing connected sub devices like Neopixel rings.
    """
    def __init__(self, neopixels, ir, led, uart):
        self.neopixels = neopixels
        self.ir = ir
        self.led = led
        self.uart = uart
