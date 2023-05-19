from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from enums.mode_state_enum import ModeStateEnum
from globals import OFF_COLOR, DEFAULT_FADE


class Fade(AnimatedMode):
    def __init__(self, device: Device, desired_state: DeviceState, colors=DEFAULT_FADE):
        super().__init__(device, desired_state)
        self.brightness = desired_state.brightness
        self._itr = 0
        self._i = 0
        self._max = desired_state.speed
        self._strip_colors = [device.strip[i] for i in range(len(device.strip))]
        self.colors = [tuple(x) for x in colors]
        self.color = self.colors[0]

    def end(self):
        self.state = ModeStateEnum.ENDING
        self._default()

    def end_step(self):
        self._itr += 1
        self._animate(OFF_COLOR.rgb_color)
        if self._itr == self._max:
            self.state = ModeStateEnum.OFF

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._default()

    def start_step(self):
        self._itr += 1
        self._animate(self.color)
        if self._itr == self._max:
            self._default_end_step()

    def step(self):
        self._itr += 1
        self._animate(self.color)

        if self._itr == self._max:
            self._itr = 0 
            self._i += 1
            if self._i == len(self.colors):
                self._i = 0
            self.color = self.colors[self._i]
            
            self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def update(self, json):
        self.state = ModeStateEnum.UPDATING
        if json is not None:
            if "colors" in json:
                tmp_colors = json["colors"]
                if len(tmp_colors) > 2:
                    self.colors = [tuple(x) for x in tmp_colors]

        self._itr = 0
        self._i = 0
        self.color = self.colors[self._i]
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def update_step(self):
        self._itr += 1
        self._animate(self.color)
        
        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self._itr = 0 
            self._i += 1
            if self._i == len(self.colors):
                self._i = 0
            self.color = self.colors[self._i]
            
            self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def _default(self):
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def _default_end_step(self):
        self.state = ModeStateEnum.ON
        self._itr = 0
        self._i += 1
        self._i = self._i % len(self.colors)
        self.color = self.colors[self._i]
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

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
