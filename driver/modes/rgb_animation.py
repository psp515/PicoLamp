from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from enums.mode_state_enum import ModeStateEnum
from globals import OFF_COLOR
from utime import sleep_ms

class RGB(AnimatedMode):
    color: ()

    def __init__(self, device: Device, desired_state: DeviceState, wait=0):
        super().__init__(device, desired_state)
        self.brightness = desired_state.brightness
        self._itr = 0
        self._max = self._desired_state.speed
        self._rgb_max = 255
        self._wait = wait
        self._strip_colors = [device.strip[i] for i in range(len(device.strip))]
        self._starting_colors = []
        self._ending_colors = [OFF_COLOR.rgb_color for _ in range(len(device.strip))]

        for group in self._device.np_groups:
            for i, led in enumerate(group):
                pos = (i * 256 // len(group))
                self._starting_colors.append(self._wheel(pos & 255))

    def end(self):
        self.state = ModeStateEnum.ENDING
        self._default()

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._default()

    def _default(self):
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def start_step(self):
        self._itr += 1
        self._animate(self._starting_colors)

        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self._itr = 0

    def end_step(self):
        self._itr += 1
        self._animate(self._ending_colors)
        if self._itr == self._max:
            self.state = ModeStateEnum.OFF
            self._itr = 0        

    def update(self, json):
        if json is not None:
            if "wait" in json:
                self._wait = json["wait"]

    def update_step(self): pass

    def refresh_led(self): pass

    def step(self):
        self._itr += 1
        self._rgb_animate()
        if self._itr == self._rgb_max:
            self._itr = 0

    def _animate(self, colors):
        n = self._desired_state.speed
        rising, downing = self._itr / n, (n - self._itr) / n

        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            if state:
                for led in group:
                    led_prev = self._strip_colors[led]
                    led_next = colors[led]
                    bright = self._desired_state.brightness
                    color = tuple([int(downing * led_prev[i] + rising * led_next[i] * bright) for i in range(3)])
                    self._device.strip[led] = color

        self._device.strip.write()

    def _rgb_animate(self):
        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            if state:
                for i, led in enumerate(group):
                    pos = (i * 256 // len(group)) + self._itr
                    color = self._wheel(pos & 255)
                    self._device.strip[led] = tuple(int(x * self._desired_state.brightness) for x in color)
            else:
                for led in group:
                    self._device.strip[led] = OFF_COLOR.rgb_color

        sleep_ms(self._wait)
        self._device.strip.write()

    @staticmethod
    def _wheel(pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
