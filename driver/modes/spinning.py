from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from enums.mode_state_enum import ModeStateEnum
from globals import OFF_COLOR, DEFAULT_SPIN


class Spinning(AnimatedMode):
    color: ()

    def __init__(self, device: Device, desired_state: DeviceState, colors=DEFAULT_SPIN):
        super().__init__(device, desired_state)
        self.colors = [tuple(x) for i, x in enumerate(colors) if i < 5]
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]
        self._group_counter = None

    def end(self):
        self.state = ModeStateEnum.ENDING

        for group in self._device.np_groups:
            for led in group:
                self._device.strip[led] = OFF_COLOR.rgb_color
        self._device.strip.write()

        self.state = ModeStateEnum.OFF

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._itr = 0
        self._max = self._desired_state.speed

        for group in self._device.np_groups:
            for led in group:
                if self._device.strip[led] != OFF_COLOR.rgb_color:
                    self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]
                    return

        self.state = ModeStateEnum.ON

    def start_step(self):
        self._itr += 1
        self._animate()
        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self._itr = 0
            self._group_counter = [0 for _ in range(len(self._device.np_groups))]

    def step(self):

        self._itr += 1

        for i in range(3):
            group, state = self._device.np_groups[i], self._desired_state.groups_state[i]

            actual = int((self._itr * len(group)) / self._max)
            for i in range(len(group)):
                idx = (actual + i) % len(group)
                if i < len(self.colors) and state:
                    self._device.strip[group[0] + idx] = self._calc_color(self.colors[i])
                else:
                    self._device.strip[group[0] + idx] = OFF_COLOR.rgb_color

        self._device.strip.write()

        if self._itr == self._max:
            self._itr = 0

    def _calc_color(self, color):
        return tuple([int(self._desired_state.brightness * x) for x in color])

    def update(self, json):
        if json is not None:
            if "colors" in json:
                tmp_colors = json["colors"]
                if len(tmp_colors) > 0:
                    self.colors = [tuple(x) for i, x in enumerate(tmp_colors) if i < 5]

        self.state = ModeStateEnum.ON

    def _animate(self):
        n = self._desired_state.speed
        rising, downing = self._itr / n, (n - self._itr) / n

        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            if state:
                for led in group:
                    led_prev = self._strip_colors[led]
                    led_next = OFF_COLOR.rgb_color
                    bright = self._desired_state.brightness
                    color = tuple([int(downing * led_prev[i] + rising * led_next[i] * bright) for i in range(3)])
                    self._device.strip[led] = color

        self._device.strip.write()