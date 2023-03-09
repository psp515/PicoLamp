from ujson import loads

from device import Device
from device_state import DeviceState
from models.color import Color
from modes.mode import Mode
from modes.mode_state_enum import ModeStateEnum


class ConstantColor(Mode):

    color: Color

    def __init__(self, device: Device, device_state: DeviceState, color: Color):
        super().__init__(device, device_state)
        self.color = color
        self.r, self.g, self.b = 0, 0, 0

    def start_step(self):
        pass

    def step(self):
        pass

    def update_step(self):
        pass

    def end_step(self):
        pass

    def update(self, json):
        self.state = ModeStateEnum.UPDATE
        data = loads(json)
        self.color = data["color"]
