import _thread

from device import Device
from device_state import DeviceState
from modes.constant_color import ConstantColor
from modes.mode import Mode
from modes.mode_state_enum import ModeStateEnum


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
            if self.device_state.change_mode:
                # TODO change mode
                pass

            if self.device_state.update_mode:
                self._mode.update(self.device_state.update_json)

            if self._mode.state is ModeStateEnum.START:
                self._mode.start_step()
            elif self._mode.state is ModeStateEnum.END:
                self._mode.end_step()
            elif self._mode.state is ModeStateEnum.UPDATE:
                self._mode.update_step()
            else:
                self._mode.step()
