from device import Device
from device_state import DeviceState
from globals import DEFAULT_COLOR, OFF_COLOR
from models.color import Color
from modes.mode import Mode
from enums.mode_state_enum import ModeStateEnum

# TODO: Fix
class ConstantColor(Mode):
    color: ()

    def __init__(self, device: Device, device_state: DeviceState, color: Color = DEFAULT_COLOR):
        super().__init__(device, device_state)
        self.color = color.rgb_color
        self.itr = 0

    def start_step(self):
        self.itr += 1
        self._applicate(self.color)

        if self.itr == self._desired_state.speed:
            self.itr = 0
            self.state = ModeStateEnum.ON

    def update_step(self):
        self.itr += 1
        self._applicate(self.color)

        if self.itr == self._desired_state.speed:
            self.itr = 0
            self.state = ModeStateEnum.ON

    def end_step(self):
        self.itr += 1
        self._applicate(OFF_COLOR.rgb_color)

        if self.itr == self._desired_state.speed:
            self.itr = 0
            self.state = ModeStateEnum.OFF

    def update(self):
        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            for led_id in group:
                if state:
                    color = tuple([int(x * self._desired_state.brightness) for x in self.color])
                else:
                    color = OFF_COLOR.rgb_color
                self._device.strip[led_id] = color

        self._device.strip.write()

    def extended_update(self, data: {}):
        self.state = ModeStateEnum.UPDATING
        new_color = data["r"], data["g"], data["b"]

        if new_color != self.color:
            self.color = new_color

        self.state = ModeStateEnum.UPDATING
        self.itr = 0

    def end(self):
        self.state = ModeStateEnum.ENDING
        self.itr = 0

    def start(self):
        self.state = ModeStateEnum.STARTING
        self.itr = 0

    def refresh_led(self):
        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            if not state:
                for led_id in group:
                    self._device.strip[led_id] = OFF_COLOR.rgb_color

    def _applicate(self, to_color: ()):
        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            for led_id in group:
                act = self._device.strip[led_id]
                color = tuple([self._get_factor(act[i], to_color[i]) for i in range(3)])
                self._device.strip[led_id] = color if state else OFF_COLOR.rgb_color

        self._device.strip.write()

    def _get_factor(self, act, dest):
        n = self._desired_state.speed
        brightness = (self._desired_state.brightness * self.itr + (n - self.itr) * self._desired_state.old_brightness) // n
        color = (self.itr * dest + (n - self.itr) * act) // n
        return color * brightness

