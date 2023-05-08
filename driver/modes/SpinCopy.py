from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from enums.mode_state_enum import ModeStateEnum
from globals import LOADING_SPAN, OFF_COLOR, device_colors
from time import ticks_ms, ticks_diff, ticks_add


class Spinning(AnimatedMode):
    color: ()

    def __init__(self, device: Device, desired_state: DeviceState, colors=device_colors, speed=None):
        super().__init__(device, desired_state)
        self.colors = [tuple(x) for i, x in enumerate(colors) if i < 5]
        self.speed = LOADING_SPAN if speed is None else max(speed, LOADING_SPAN)
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]
        self._starting_colors = []
        self._next = ticks_add(ticks_ms(), self.speed)
        self._group_counter = [-len(self.colors) + 1 for _ in range(len(self._device.np_groups))]

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
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def start_step(self):
        self._itr += 1
        self._animate()
        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self._itr = 0
            self._group_counter = [0 for _ in range(len(self._device.np_groups))]

    def step(self):
        if ticks_diff(ticks_ms(), self._next) < 0:
            return

        for i in range(3):
            group, state = self._device.np_groups[i], self._desired_state.groups_state[i]

            for led in group:
                self._device.strip[led] = OFF_COLOR.rgb_color

            if state:
                first = group[0]
                for j in range(len(self.colors)):
                    idx = (self._group_counter[j] + j) % len(group)
                    if idx < 0:
                        continue
                    self._device.strip[idx + first] = self._calc_color(self.colors[j])

            self._group_counter[i] += 1

            if self._group_counter[i] == len(group):
                self._group_counter[i] = 0

        self._device.strip.write()

        self._next = ticks_add(ticks_ms(), self.speed)

    def _calc_color(self, color):
        return tuple([int(self._desired_state.brightness * x) for x in color])

    def update(self, json):
        if json is not None:
            if "speed" in json:
                self.speed = max(json["speed"], LOADING_SPAN)
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