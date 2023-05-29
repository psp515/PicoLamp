from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from enums.mode_state_enum import ModeStateEnum
from globals import LOADING_SPAN, OFF_COLOR, DEVICE_COLORS, DEFAULT_FADE
from time import ticks_ms, ticks_diff, ticks_add


class Loading(AnimatedMode):
    
    def __init__(self, device: Device, desired_state: DeviceState, colors=DEFAULT_FADE, speed=None):
        super().__init__(device, desired_state)
        self.colors = [tuple(x) for x in colors]
        self.speed = LOADING_SPAN if speed is None else max(speed, LOADING_SPAN)
        self.color = tuple(self.colors[0])
        self._itr = 0
        self._max = self._desired_state.speed
        self._is_shining = True
        self.groups_state = desired_state.groups_state
        self._next = ticks_add(ticks_ms(), self.speed)
        self.brightness = desired_state.brightness
        self._strip_colors = [device.strip[i] for i in range(len(device.strip))]

    def end(self):
        self.state = ModeStateEnum.ENDING

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._is_shining = True
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def update(self, json):
        if json is not None:
            if "speed" in json:
                self.speed = max(json["speed"], LOADING_SPAN)
            if "colors" in json:
                tmp_colors = json["colors"]
                if len(tmp_colors) > 0:
                    self.colors = [tuple(x) for x in tmp_colors]
        
        self.state = ModeStateEnum.ON

    def start_step(self):
        self._itr += 1
        self._animate(self.color)
        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self._itr = 0

    def update_step(self): pass

    def step(self):

        if ticks_diff(ticks_ms(), self._next) < 0:
            return

        self._itr += 1
        if self._is_shining:
            for group, state in zip(self._device.np_groups, self.groups_state):
                first = group[0]
                actual = int(first + self._itr * len(group) / self._max)
                actual = min(actual, len(self._device.strip) - 1)
                self._device.strip[actual] = OFF_COLOR.rgb_color
        else:
            for group, state in zip(self._device.np_groups, self.groups_state):
                if state:
                    first = group[0]
                    actual = int(first + (self._itr * len(group)) / self._max)
                    actual = min(actual, len(self._device.strip) - 1)
                    self._device.strip[actual] = self._calc_color(self.color)
                    
        self._device.strip.write()

        self._next = ticks_add(ticks_ms(), self.speed)

        if self._itr == self._max:
            self._is_shining = not self._is_shining
            self._itr = 0
            self.groups_state = self._desired_state.groups_state
            self.brightness = self._desired_state.brightness
            if not self._is_shining:
                i = ticks_ms() % len(self.colors)
                if self.colors[i] == self.color:
                    i = (i + 1) % len(self.colors)
                self.color = self.colors[i]

    def _calc_color(self, color):
        return tuple([int(self.brightness * x) for x in color])

    def end_step(self):
        self.step()
        if self._itr == 0 and not self._is_shining:
            self.state = ModeStateEnum.OFF

    def refresh_led(self): pass

    def _animate(self, to_color: ()):
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
                    color = tuple([int(downing * led_prev[i] + rising * to_color[i] * bright) for i in range(3)])
                    self._device.strip[led] = color
            else:
                for led in group:
                    self._device.strip[led] = OFF_COLOR.rgb_color

        self._device.strip.write()