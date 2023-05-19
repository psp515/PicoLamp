from enums.device_state_enum import DeviceStateEnum


class DeviceState:
    """Class purpose is to represent designated state of the device."""
    def __init__(self, n):
        self.brightness_prev = 1
        self.brightness = 1
        self.speed = 200
        self.groups_state = [True] * n

        self.state = DeviceStateEnum.OFF

        self.mode = None
        self.json = None

        self.push_device_state = False
        self.ir = None
        
        self.wifi = []
