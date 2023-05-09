from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from enums.mode_state_enum import ModeStateEnum
from globals import OFF_COLOR, TORCH_MAX
import random


class Torch(AnimatedMode):
    def __init__(self, device: Device, desired_state: DeviceState):
        super().__init__(device, desired_state)
        self.brightness = desired_state.brightness
        self._itr = 0
        self._max = desired_state.speed // 10
        self._strip_colors = [device.strip[i] for i in range(len(device.strip))]
        self._colors = [self._generate_color() for _ in range(len(device.strip))]

    def end(self):
        self.state = ModeStateEnum.ENDING
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def end_step(self):
        self._itr += 1
        self._animate()
        if self._itr == self._max:
            self.state = ModeStateEnum.OFF

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]
        self._colors = [OFF_COLOR.rgb_color for _ in range(len(self._device.strip))]
        self._itr = 0
        self._max = self._desired_state.speed

    def start_step(self):
        self._itr += 1
        self._animate()
        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self._max = self._desired_state.speed // 10
            self._itr = 0
            self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]
            self._colors = [OFF_COLOR.rgb_color for _ in range(len(self._device.strip))]

    def step(self):
        self._itr += 1
        self._animate()

        if self._itr == self._max:
            self._max = self._desired_state.speed // 10
            self._itr = 0
            self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]
            self._colors = [OFF_COLOR.rgb_color for _ in range(len(self._device.strip))]

    def update(self, json): pass

    def refresh_led(self): pass

    def _generate_color(self):
        r, g, b = TORCH_MAX
        value = random.randint(0, 100)

        r = r - value
        g = r - 5
        b = b - value // 5

        return r, g, b

    def _animate(self):
        n = self._desired_state.speed
        rising, downing = self._itr / n, (n - self._itr) / n

        if self._desired_state.brightness_prev == self._desired_state.brightness:
            bright = self._desired_state.brightness
        else:
            bright = (rising * self._desired_state.brightness + downing * self._desired_state.brightness_prev)

        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            if state:
                for led in group:
                    led_prev = self._strip_colors[led]
                    led_next = self._colors[led]
                    color = tuple([int(downing * led_prev[i] + rising * led_next * bright) for i in range(3)])
                    self._device.strip[led] = color
            else:
                for led in group:
                    self._device.strip[led] = OFF_COLOR.rgb_color

        self._device.strip.write()
