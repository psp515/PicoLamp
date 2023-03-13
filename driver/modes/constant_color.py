from ujson import loads

from device import Device
from device_state import DeviceState
from globals import DEFAULT_COLOR
from models.color import Color
from modes.mode import Mode
from enums.mode_state_enum import ModeStateEnum


class ConstantColor(Mode):
    color: Color

    def __init__(self, device: Device, device_state: DeviceState, color: Color = DEFAULT_COLOR):
        super().__init__(device, device_state)
        self.dest_color = color.rgb_color
        self.act_col = (0, 0, 0)
        self.last_col = (0, 0, 0)
        self.itr = 0

    def start_step(self):
        self.itr += 1
        self.act_col = tuple([self._get_factor(0, self.dest_color[i]) for i in range(3)])
        self._apply_color(self.act_col)

        if self.itr == self._device_state.speed:
            self.itr = 0
            self.state = ModeStateEnum.NORMAL

    def step(self):
        #TODO: resolve brightness
        pass

    def update_step(self):
        self.act_col = tuple([self._get_factor(self.last_col[i], self.dest_color[i]) for i in range(3)])
        self._apply_color(self.act_col)

        if self.itr == self._device_state.speed:
            self.itr = 0
            self.state = ModeStateEnum.NORMAL

    def end_step(self):
        self.act_col = tuple([self._get_factor(self.act_col[i], 0) for i in range(3)])
        self._apply_color(self.act_col)

        if self.itr == self._device_state.speed:
            self.itr = 0
            self.state = ModeStateEnum.OFF

    def update(self, data: {}):
        self.state = ModeStateEnum.UPDATE
        new_color = Color(data["r"], data["g"], data["b"], data["name"])

        if not self.dest_color.same(new_color):
            self.dest_color = new_color
            self.last_col = self.act_col
            self.state = ModeStateEnum.UPDATE
            self.itr = 0

    def _apply_color(self, color: ()):
        for group, state in zip(self._device.np_groups, self._device_state.groups_state):
            if state:
                for led_id in group:
                    self._device.strip[led_id] = color

        self._device.strip.write()

    def _get_factor(self, act, dest):
        n = self._device_state.speed
        i = self.itr
        value = i * dest + (n - i) * act
        return int(value * self._device_state.brightness)
