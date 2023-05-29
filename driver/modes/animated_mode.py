from device import Device
from device_state import DeviceState
from enums.mode_state_enum import ModeStateEnum
from modes.mode import Mode


class AnimatedMode(Mode):
    def __init__(self, device: Device, desired_state: DeviceState):
        super(AnimatedMode, self).__init__(device, desired_state)
        self.brightness = desired_state.brightness

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

    def refresh_led(self):
        """
        Function ignored.
        (most modes will update number of working led-s dynamically)
        """
        pass
