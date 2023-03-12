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

    def start(self):
        _thread.start_new_thread(self._loop(), ())

    def _loop(self):
        while True:
            if self.device_state.status == DeviceStateEnum.OFF:
                if self._mode.state != ModeStateEnum.END and self._mode.state != ModeStateEnum.OFF:
                    self._mode.state = ModeStateEnum.END

                if self._mode.state == ModeStateEnum.END:
                    self._mode.end_step()

            elif self.device_state.status == DeviceStateEnum.NEW_MODE:
                # TODO: 2 options animate leaving or quick change.

                self.device_state.status = DeviceStateEnum.ON
            elif self.device_state.status == DeviceStateEnum.UPDATE_MODE:
                self._mode.update(self.device_state.update_json)
                self.device_state.status = DeviceStateEnum.ON
            else:
                if self._mode.state == ModeStateEnum.START:
                    self._mode.start_step()
                elif self._mode.state == ModeStateEnum.UPDATE:
                    self._mode.update_step()
                else:
                    self._mode.step()
