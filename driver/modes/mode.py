from device import Device
from device_state import DeviceState
from enums.mode_state_enum import ModeStateEnum


class Mode:

    _device: Device
    _n: int

    def __init__(self, device: Device,
                 device_state: DeviceState):
        self._device_state = device_state
        self._device = device
        self.state = ModeStateEnum.START

    def start_step(self):
        pass

    def step(self):
        pass

    def update_step(self):
        pass

    def end_step(self):
        pass

    def update_brightness(self):
        pass

    def update(self, json):
        self.state = ModeStateEnum.UPDATE