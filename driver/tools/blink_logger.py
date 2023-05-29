from machine import Pin
from utime import sleep

from enums.logger_enum import LoggerEnum
from tools.logger import Logger


class BlinkLogger(Logger):
    def __init__(self, led: Pin, debug: bool):
        super().__init__(debug)
        self._led = led

    def log(self, message: str, information: LoggerEnum):
        if information == LoggerEnum.DEBUG:
            if self.debug:
                print(f"DEBUG: {message}")
        else:
            actions = self.get_information_data(information)
            print(f"{actions[0]} - {actions[1]}: {message}")
            self._blink(actions[0])

    def _blink(self, n: int):
        for i in range(n):
            self._led.value(1)
            sleep(0.1)
            self._led.value(0)
            sleep(0.1)

