from machine import Pin, UART
from utime import sleep

from device import Device
from logger_enum import LoggerEnum


class Logger:
    def __init__(self, device: Device):
        self._device = device

    def log(self, message: str, information: LoggerEnum):
        print(message)
        self._device.uart.write(message)
        self._blink(information)

    def _blink(self, n: int):
        for i in range(n):
            self._device.led.value(1)
            sleep(0.1)
            self._device.led.value(0)
            sleep(0.1)