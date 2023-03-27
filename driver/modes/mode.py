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
        self.state = ModeStateEnum.OFF

    def loop(self):
        pass

    def end(self):
        self.state = ModeStateEnum.ENDING

    def start(self):
        self.state = ModeStateEnum.STARTING

    def update(self, json):
        self.state = ModeStateEnum.UPDATING

    def refresh_led(self):
        self.state = ModeStateEnum.UPDATING

