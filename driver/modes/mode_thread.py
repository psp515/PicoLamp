from device import Device
from device_state import DeviceState
from enums.device_state_enum import DeviceStateEnum
from enums.logger_enum import LoggerEnum
from modes.constant_color import ConstantColor
from modes.blink import Blink
from modes.instant_blink import InstantBlink
from modes.constant_color_na import ConstantColorNA
from modes.torch import Torch
from modes.wifi_quality import WifiQuality
from modes.fade import Fade
from modes.spinning import Spinning
from modes.rgb_animation import RGB
from modes.loading import Loading
from enums.mode_state_enum import ModeStateEnum
from tools.blink_logger import Logger


class ModeThread:

    def __init__(self,
                 device: Device,
                 states: DeviceState,
                 logger: Logger):
        self._device = device
        self._logger = logger
        self._states = states
        self._mode = ConstantColor(device, states)
        self._mode_num = 1

    def loop(self):
        self._logger.log("Mode Thread: Starting.", LoggerEnum.INFO)
        self._restart_strip()

        while True:
            if self._states.state == DeviceStateEnum.ENDING:
                self._mode.end()
                self._logger.log("Device to switch OFF.", LoggerEnum.INFO)
                self._states.state = DeviceStateEnum.OFF
            elif self._states.state == DeviceStateEnum.STARTING:
                self._mode.start()
                self._logger.log("Device starting.", LoggerEnum.INFO)
                self._states.state = DeviceStateEnum.ON
            elif self._states.state == DeviceStateEnum.NEW:
                self._change_mode()
                self._logger.log("Device new mode.", LoggerEnum.INFO)
                self._states.state = DeviceStateEnum.ON
            elif self._states.state == DeviceStateEnum.UPDATE:
                self._mode.update(self._states.json)
                self._states.json = None
                self._logger.log("Device updating.", LoggerEnum.INFO)
                self._states.state = DeviceStateEnum.ON
            elif self._states.state == DeviceStateEnum.LED_UPDATE:
                self._mode.refresh_led()
                self._logger.log("Device led update.", LoggerEnum.INFO)
                self._states.state = DeviceStateEnum.ON

            self._mode.loop()

    def _change_mode(self):
        mode = self._states.mode
        
        if mode == self._mode_num:
            return

        json = self._states.json
        
        if mode > 9 or mode < 0:
            mode = -1

        try:
            if mode == -1 or mode == 0:
                if self._states.json is not None and "color" in json:
                    self._mode = ConstantColorNA(self._device, self._states, self._states.json["color"])
                else:
                    print("here")
                    self._mode = ConstantColorNA(self._device, self._states)
                self._mode_num = 0
            elif mode == 1:
                if self._states.json is not None and "color" in json:
                    self._mode = ConstantColor(self._device, self._states, self._states.json["color"])
                else:
                    self._mode = ConstantColor(self._device, self._states)
                self._mode_num = 1
            elif mode == 2:
                if self._states.json is not None and "speed" in json and "colors" in json and len(json["colors"]) > 0:
                    self._mode = Blink(self._device, self._states, self._states.json["colors"],
                                       self._states.json["speed"])
                else:
                    self._mode = Blink(self._device, self._states)
                self._mode_num = 2
            elif mode == 3:
                if self._states.json is not None and "speed" in json and "colors" in json and len(json["colors"]) > 0:
                    self._mode = InstantBlink(self._device, self._states, self._states.json["colors"],
                                              self._states.json["speed"])
                else:
                    self._mode = InstantBlink(self._device, self._states)
                self._mode_num = 3
            elif mode == 4:
                if self._states.json is not None and "speed" in json and "colors" in json and len(json["colors"]) > 0:
                    self._mode = Loading(self._device, self._states, self._states.json["colors"],
                                         self._states.json["speed"])
                else:
                    self._mode = Loading(self._device, self._states)
                self._mode_num = 4
            elif mode == 5:
                if self._states.json is not None and "wait" in json:
                    self._mode = RGB(self._device, self._states, self._states.json["wait"])
                else:
                    self._mode = RGB(self._device, self._states)
                self._mode_num = 5
            elif mode == 6:
                if self._states.json is not None and "colors" in json and len(json["colors"]) > 0:
                    self._mode = Spinning(self._device, self._states, self._states.json["colors"])
                else:
                    self._mode = Spinning(self._device, self._states)
                self._mode_num = 6
            elif mode == 7:
                if self._states.json is not None and "colors" in json and len(json["colors"]) > 2:
                    self._mode = Fade(self._device, self._states, self._states.json["colors"])
                else:
                    self._mode = Fade(self._device, self._states)
                self._mode_num = 7
            elif mode == 8:
                self._mode = WifiQuality(self._device, self._states)
                self._mode_num = 8
            elif mode == 9:
                self._mode = Torch(self._device, self._states)
                self._mode_num = 9
        except TypeError as e:
            self._logger.log(f"Mode Thread: {e}", LoggerEnum.ERROR)
            self._logger.log(f"Mode Thread: Mode didn't changed.", LoggerEnum.INFO)
    
        self._mode.state = ModeStateEnum.STARTING
        
    def _restart_strip(self):
        for group in self._device.np_groups:
            for led_id in group:
                self._device.strip[led_id] = (0, 0, 0)

        self._logger.log("Mode Thread: Device refreshed.", LoggerEnum.INFO)
        self._device.strip.write()
