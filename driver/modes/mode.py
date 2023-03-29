from device import Device
from device_state import DeviceState
from enums.mode_state_enum import ModeStateEnum


class Mode:
    _device: Device

    def __init__(self, device: Device,
                 desired_state: DeviceState):
        self._desired_state = desired_state
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

