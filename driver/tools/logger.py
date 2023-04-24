from machine import Pin
from utime import sleep

from enums.logger_enum import LoggerEnum


class Logger:
    def __init__(self, led: Pin, debug: bool):
        self.debug = debug
        self._led = led

    def log(self, message: str, information: LoggerEnum):
        #if information != LoggerEnum.DEBUG or (self.debug and information == information.DEBUG):
        print(message)
        # TODO Consider to blink only if debug
        # self._blink(1)

    def _blink(self, n: int):
        for i in range(n):
            self._led.value(1)
            sleep(0.1)
            self._led.value(0)
            sleep(0.1)

