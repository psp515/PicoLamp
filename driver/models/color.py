

class Color:
    def __init__(self, r, g, b, name):
        self._r = r
        self._g = g
        self._b = b
        self._name = name

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @property
    def name(self):
        return self._name

    @property
    def rgb_color(self):
        return self._r, self._g, self._b


