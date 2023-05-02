from device import Device
from device_state import DeviceState
from enums.device_state_enum import DeviceStateEnum
from enums.logger_enum import LoggerEnum
from modes.constant_color import ConstantColor
from modes.constant_color_na import ConstantColorNA
from modes.mode import Mode
from enums.mode_state_enum import ModeStateEnum
from tools.logger import Logger


class ModeThread:
    _mode: Mode

    def __init__(self,
                 device: Device,
                 states: DeviceState,
                 logger: Logger):
        self._device = device
        self._logger = logger
        self._states = states
        self._mode = ConstantColorNA(device, states)
        self._mode_num = 0

    def loop(self):
        self._restart_strip()

        while True:
            if self._states.state == DeviceStateEnum.ENDING:
                self._mode.end()
                self._logger.log("Device to switch OFF.", LoggerEnum.DEBUG)
                self._states.state = DeviceStateEnum.OFF
            elif self._states.state == DeviceStateEnum.STARTING:
                self._mode.start()
                self._logger.log("Device starting.", LoggerEnum.DEBUG)
                self._states.state = DeviceStateEnum.ON
            elif self._states.state == DeviceStateEnum.NEW:
                self._change_mode()
                self._logger.log("Device new mode.", LoggerEnum.DEBUG)
                self._states.state = DeviceStateEnum.ON
            elif self._states.state == DeviceStateEnum.UPDATE:
                self._mode.update(self._states.json)
                self._states.json = None
                self._logger.log("Device updating.", LoggerEnum.DEBUG)
                self._states.state = DeviceStateEnum.ON
            elif self._states.state == DeviceStateEnum.LED_UPDATE:
                self._mode.refresh_led()
                self._logger.log("Device led update.", LoggerEnum.DEBUG)
                self._states.state = DeviceStateEnum.ON

            self._mode.loop()

    def _change_mode(self):
        mode = self._states.mode
        
        if mode == self._mode_num:
            return
        
        if mode == -1 or mode == 0:
            if self._states.json is not None:
                self._mode = ConstantColorNA(self._device, self._states, self._states.json["color"])
            else:
                self._mode = ConstantColorNA(self._device, self._states)
            self._mode_num = 0
        elif mode == 1:
            print("here")
            if self._states.json is not None:
                self._mode = ConstantColor(self._device, self._states, self._states.json["color"])
            else:
                self._mode = ConstantColor(self._device, self._states)
            self._mode_num = 1
                
        self._mode.state = ModeStateEnum.STARTING
        
    def _restart_strip(self):
        for group in self._device.np_groups:
            for led_id in group:
                self._device.strip[led_id] = (0, 0, 0)

        self._logger.log("Device refreshed.", LoggerEnum.INFO)
        self._device.strip.write()
