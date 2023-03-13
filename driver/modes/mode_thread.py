import _thread

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
        while True:
            if self.device_state.state == DeviceStateEnum.OFF:
                if self._mode.state != ModeStateEnum.ENDING and self._mode.state != ModeStateEnum.OFF:
                    self._mode.end()
            elif self.device_state.state == DeviceStateEnum.NEW_MODE:
                # TODO: change mode
                self.device_state.state = DeviceStateEnum.ON
            elif self.device_state.state == DeviceStateEnum.UPDATE_MODE:
                self._mode.update(self.device_state.update_json)
                self.device_state.state = DeviceStateEnum.ON
            elif self.device_state.state == DeviceStateEnum.STARTING:
                self.device_state.state = DeviceStateEnum.ON
                self._mode.start()

            if self._mode.state == ModeStateEnum.STARTING:
                self._mode.start_step()
            elif self._mode.state == ModeStateEnum.UPDATE:
                self._mode.update_step()
            elif self._mode.state == ModeStateEnum.ENDING:
                self._mode.end_step()
            elif self._mode.state == ModeStateEnum.NORMAL:
                self._mode.step()
