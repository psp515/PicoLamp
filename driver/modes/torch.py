from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from enums.mode_state_enum import ModeStateEnum
from globals import OFF_COLOR, TORCH_MAX, DEFAULT_TORCH
import random


class Torch(AnimatedMode):
    def __init__(self, device: Device, desired_state: DeviceState):
        super().__init__(device, desired_state)
        self.brightness = desired_state.brightness
        self._itr = 0
        self._i = 0
        self._max = desired_state.speed // 10
        self._strip_colors = [device.strip[i] for i in range(len(device.strip))]
        self._color = None

    def end(self):
        self.state = ModeStateEnum.ENDING
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def end_step(self):
        self._itr += 1
        self._animate(OFF_COLOR.rgb_color)
        if self._itr == self._max:
            self.state = ModeStateEnum.OFF

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]
        self._itr = 0
        self._max = self._desired_state.speed

    def start_step(self):
        self._itr += 1
        self._animate(TORCH_MAX)
        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self._max = self._desired_state.speed // random.randint(10, 30)
            self._itr = 0
            self._strip_colors = [OFF_COLOR.rgb_color for _ in range(len(self._device.strip))]
            self._color = self._generate_color()
            print(self._color, self._max)

    def step(self):
        self._itr += 1
        self._animate(self._color)

        if self._itr == self._max:
            self._max = self._desired_state.speed // random.randint(10, 30)
            self._itr = 0
            self._i += 1
            if self._i == len(DEFAULT_TORCH):
                self._i = 0
            self._color = DEFAULT_TORCH[self._i]
            self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def update(self, json): pass

    def refresh_led(self): pass

    @staticmethod
    def _generate_color():
        r, g, b = TORCH_MAX
        value = random.randint(0, 100)

        r = r - value
        g = r - 5
        b = b - value // 5

        return r, g, b

    def _animate(self, to_color: ()):
        n = self._max
        rising, downing = self._itr / n, (n - self._itr) / n

        bright = self._desired_state.brightness

        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            if state:
                for led in group:
                    led_prev = self._strip_colors[led]
                    color = tuple([int(downing * led_prev[i] + rising * to_color[i] * bright) for i in range(3)])
                    self._device.strip[led] = color
            else:
                for led in group:
                    self._device.strip[led] = OFF_COLOR.rgb_color

        self._device.strip.write()
