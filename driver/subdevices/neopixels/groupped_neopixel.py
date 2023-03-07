from neopixel import NeoPixel

# TODO fix import when class ready


class GrouppedNeopixel(NeoPixel):
    @property
    def brightness(self):
        """
        """
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        if value < 0:
            self._brightness = 0
        elif value > 1:
            self._brightness = 1
        else:
            self._brightness = value