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
        if self.state == ModeStateEnum.STARTING:
            self.start_step()
        elif self.state == ModeStateEnum.UPDATE:
            self.update_step()
        elif self.state == ModeStateEnum.ENDING:
            self.end_step()
        elif self.state == ModeStateEnum.NORMAL:
            self.step()

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

    def end(self):
        self.state = ModeStateEnum.ENDING

    def start(self):
        self.state = ModeStateEnum.STARTING

    def extended_update(self, json):
        self.state = ModeStateEnum.UPDATE

    def refresh(self):
        pass
