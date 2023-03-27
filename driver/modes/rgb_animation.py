from device import Device
from device_state import DeviceState
from modes.mode import Mode


class RGBAnimation(Mode):

    def __init__(self, device: Device, device_state: DeviceState):
        super().__init__(device, device_state)
        self.itr = 0

