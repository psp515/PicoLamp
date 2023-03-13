from enums.device_state_enum import DeviceStateEnum


class DeviceState:
    """Class purpose is to represent designated state of the device."""
    def __init__(self, n):
        self.brightness = 1
        self.speed = 128
        self.groups_state = [True] * n

        self.state = DeviceStateEnum.OFF

        self.mode_json = ""
        self.update_json = ""

        self.push_device_state = False
