from machine import Pin
from utime import sleep

from enums.logger_enum import LoggerEnum


class Logger:
    def __init__(self, led: Pin, debug: bool):
        self.debug = debug
        self._led = led

    def log(self, message: str, information: LoggerEnum):
        if information == LoggerEnum.DEBUG:
            if self.debug:
                print(f"DEBUG: {message}")
        else:
            actions = self._get_information_data(information)
            print(f"{actions[1]}: {message}")
            self._blink(actions[0])
    
    @staticmethod
    def _get_information_data(information: LoggerEnum):
        if information == LoggerEnum.INFO:
            return 0, "INFO"
        elif information == LoggerEnum.WARNING:
            return 1, "WARNING"
        elif information == LoggerEnum.ERROR:
            return 2, "ERROR"
        elif information == LoggerEnum.SETUP_ERROR:
            return 3, "SETUP ERROR"
        elif information == LoggerEnum.CONNECTION_ERROR:
            return 4, "CONNECTION ERROR"
        
        return 0, "DEBUG"

    def _blink(self, n: int):
        for i in range(n):
            self._led.value(1)
            sleep(0.1)
            self._led.value(0)
            sleep(0.1)

