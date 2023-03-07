from machine import Pin, UART, reset
from app import App
from utime import sleep

import gc
import network

from device import Device
from exception.setup_error import SetupError
from tools.logger import Logger
from tools.logger_enum import LoggerEnum
from tools.helpers import read_json

if __name__ == '__main__':
    gc.collect()

    try:
        # TODO initialize elements
        # Devices

        uart = UART(0, tx=Pin(0), rx=Pin(1))
        led = Pin("LED", Pin.OUT)
        led.low()

        neopixel = None

        ir = None

        device = Device(neopixel, ir, led, uart)
        logger = Logger(device)

        # WIFI

        wlan_data = read_json("conf/secrets.json")

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        wlan.connect(wlan_data["ssid"], wlan_data["password"])
        sleep(1)
        i = 0

        while not wlan.isconnected() and i < 10:
            logger.log(f"Not Connected. Status: {wlan.status()}. Awaiting.", LoggerEnum.WARNING)
            i += 1
            sleep(1)

        if not wlan.isconnected():
            logger.log(f"Not Connected. Status: {wlan.status()}. ", LoggerEnum.WARNING)

        # TODO: connect to mqtt client


        # TODO: initialize default mode

        app = App()

        app.start()
    except OSError as e:
        logger.log(e, LoggerEnum.CONNECTION_ERROR)
    except Exception as e:
        logger.log(e, LoggerEnum.ERROR)
    finally:
        sleep(3)
        reset()
