from machine import Pin
from utime import sleep

from enums.logger_enum import LoggerEnum


class Logger:
    def __init__(self, led: Pin):
        self._led = led

    def log(self, message: str, information: LoggerEnum):
        print(message)
        self._blink(information)

    def _blink(self, n: int):
        for i in range(n):
            self._led.value(1)
            sleep(0.1)
            self._led.value(0)
            sleep(0.1)

