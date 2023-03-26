from device import Device
from device_state import DeviceState
from enums.device_state_enum import DeviceStateEnum
from modes.constant_color import ConstantColor
from modes.mode import Mode
from enums.mode_state_enum import ModeStateEnum


class ModeThread:
    _mode: Mode

    def __init__(self,
                 device: Device,
                 device_state: DeviceState):
        self.device = device
        self.device_state = device_state
        self._mode = ConstantColor(device, device_state)

    def loop(self):
        self._restart_strip()

        while True:
            if self.device_state.state == DeviceStateEnum.OFF:
                if self._mode.state != ModeStateEnum.ENDING and self._mode.state != ModeStateEnum.OFF:
                    self._mode.end()
            elif self.device_state.state == DeviceStateEnum.NEW:
                # TODO: change mode
                self.device_state.state = DeviceStateEnum.ON
            elif self.device_state.state == DeviceStateEnum.UPDATE:
                self._mode.refresh()
                self.device_state.state = DeviceStateEnum.ON
            elif self.device_state.state == DeviceStateEnum.EXTENDED_UPDATE:
                self._mode.extended_update(self.device_state.update_json)
                self.device_state.update_json = None
                self.device_state.state = DeviceStateEnum.ON
            elif self.device_state.state == DeviceStateEnum.STARTING:
                self.device_state.state = DeviceStateEnum.ON
                self._mode.start()

            self._mode.loop()

    def _restart_strip(self):
        for group in self.device.np_groups:
            for led_id in group:
                self.device.strip[led_id] = (0, 0, 0)

        self.device.strip.write()
