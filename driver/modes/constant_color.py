from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from modes.constant_color_na import ConstantColorNA
from enums.mode_state_enum import ModeStateEnum
from globals import DEFAULT_COLOR, OFF_COLOR


class ConstantColor(AnimatedMode, ConstantColorNA):
    color: ()
    
    def __init__(self, device: Device, desired_state: DeviceState, starting_color: () = DEFAULT_COLOR.rgb_color):
        super().__init__(device, desired_state)
        self.brightness = desired_state.brightness
        self._itr = 0
        self._max = desired_state.speed
        self._strip_colors = [device.strip[i] for i in range(len(device.strip))]
        self.color = starting_color

    def end(self):
        self.state = ModeStateEnum.ENDING
        self._default()

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._default()

    def update(self, json):
        self.state = ModeStateEnum.UPDATING
        if json is not None:
            self.color = tuple(json["color"])
        self._default()

    def _default(self):
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def start_step(self):
        self._itr += 1
        self._animate(self.color)
        if self._itr == self._max:
            self.state = ModeStateEnum.ON

    def update_step(self):
        self._itr += 1
        self._animate(self.color)
        if self._itr == self._max:
            self.state = ModeStateEnum.ON

    def end_step(self):
        self._itr += 1
        self._animate(OFF_COLOR.rgb_color)
        if self._itr == self._max:
            self.state = ModeStateEnum.OFF
    
    def refresh_led(self):
        self.state = ModeStateEnum.UPDATING
        self._write_color(self.color)
        self.state = ModeStateEnum.ON
        
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
