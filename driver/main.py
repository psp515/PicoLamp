from machine import Pin, UART, reset
from neopixel import NeoPixel

from app import App
from utime import sleep

import gc
import network

from client.hivemq_client import HivemqMQTTClient
from device import Device
from device_state import DeviceState
from exception.setup_error import SetupError
from tools.helpers import generate_groups
from tools.logger import Logger
from enums.logger_enum import LoggerEnum
from tools.config_readers import read_json, read_colors
import globals


if __name__ == '__main__':
    gc.collect()

    try:
        # Others
        globals.device_colors = read_colors("config/colors.json")

        # Device
        led = Pin("LED", Pin.OUT)
        led.low()

        strip_data = read_json("config/strip.json")

        neopixel_pin = Pin(strip_data["pin"])
        neopixel = NeoPixel(neopixel_pin, strip_data["size"])
        device_state = DeviceState(strip_data["size"])
        groups = generate_groups(strip_data["groups"], strip_data["size"])

        #TODO
        ir = None

        device = Device(neopixel, groups, ir, led)
        logger = Logger(device)
        logger.log("Logger is working!", LoggerEnum.INFO)
        # WIFI

        wlan_data = read_json("config/secrets.json")

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

        # Client

        data = read_json("config/hivemq.json")
        client = HivemqMQTTClient(data, logger, device_state)
        client.connect()

        # start app

        app = App(device, device_state, logger, client, wlan)
        logger.log("App starting!", LoggerEnum.INFO)
        app.start()

    except OSError as e:
        logger.log(str(e), LoggerEnum.CONNECTION_ERROR)
    except SetupError as e:
        logger.log(str(e), LoggerEnum.SETUP_ERROR)
    except Exception as e:
        logger.log(str(e), LoggerEnum.ERROR)
    finally:
        sleep(3)
        reset()
