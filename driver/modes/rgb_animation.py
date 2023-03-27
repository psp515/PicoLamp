from device import Device
from device_state import DeviceState
from enums.mode_state_enum import ModeStateEnum
from modes.mode import Mode


class RGBAnimation(Mode):

    def __init__(self, device: Device, device_state: DeviceState):
        super().__init__(device, device_state)
        self.itr = 0

    def loop(self):
        if self.state == ModeStateEnum.STARTING:
            self.start_step()
        elif self.state == ModeStateEnum.UPDATING:
            self.update_step()
        elif self.state == ModeStateEnum.ENDING:
            self.end_step()
        elif self.state == ModeStateEnum.ON:
            self.step()

    def start_step(self):
        pass

    def step(self):
        pass

    def update_step(self):
        pass

    def end_step(self):
        pass