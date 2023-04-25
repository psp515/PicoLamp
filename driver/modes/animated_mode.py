from device import Device
from device_state import DeviceState
from enums.mode_state_enum import ModeStateEnum


class AnimatedMode(Mode):
    def __init__(self, device: Device, desired_state: DeviceState):
        super(AnimatedMode, self).__init__(device, desired_state)
        self.brightness = desired_state.brightness
        self._itr = 0
        self._max = desired_state.speed

    def loop(self):
        if self.state == ModeStateEnum.STARTING:
            self.start_step()
        elif self.state == ModeStateEnum.UPDATING:
            self.update_step()
        elif self.state == ModeStateEnum.ENDING:
            self.end_step()
        elif self.state == ModeStateEnum.ON:
            self.step()

    def end(self):
        self.state = ModeStateEnum.ENDING
        self._default()

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._default()

    def update(self, json):
        self.state = ModeStateEnum.UPDATING
        self._default()

    def _default(self):
        self._itr = 0
        self._max = self._desired_state.speed

    def start_step(self):
        pass

    def step(self):
        pass

    def update_step(self):
        pass

    def end_step(self):
        pass

    def refresh_led(self):
        self.state = ModeStateEnum.UPDATING

