from machine import Pin, reset
from neopixel import NeoPixel

from app import App
from utime import sleep

import gc
import network

from client.hivemq_client import HivemqMQTTClient
from device import Device
from device_state import DeviceState
from exception.setup_error import SetupError
from subdevices.nec_receiver.nec_receiver import NECReceiver
from tools.helpers import generate_groups
from tools.logger import Logger
from enums.logger_enum import LoggerEnum
from tools.config_readers import read_json, read_colors
import globals


if __name__ == '__main__':
    gc.collect()

    led = Pin("LED", Pin.OUT)
    led.low()
    logger = Logger(led)
    logger.log("Logger is working!", LoggerEnum.INFO)

    try:
        # Others
        globals.device_colors = read_colors("config/colors.json")
        # TODO Validate

        # Device

        strip_data = read_json("config/strip.json")
        # TODO Validate

        neopixel_pin = Pin(strip_data["pin"])
        neopixel = NeoPixel(neopixel_pin, strip_data["size"])
        device_state = DeviceState(strip_data["size"])
        groups = generate_groups(strip_data["groups"], strip_data["size"])

        ir_data = read_json("config/pilot.json")
        # TODO Validate
        ir = NECReceiver(device_state, logger, ir_data["Pin"])

        device = Device(neopixel, groups, ir)

        # WIFI

        wlan_data = read_json("config/secrets.json")
        # TODO Validate
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

        # HiveMQ Client

        data = read_json("config/hivemq.json")
        # TODO Validate
        client = HivemqMQTTClient(data, logger, device_state)
        client.connect()

        # Ir NEC 'Client'
        #TODO: pass client to app
        # TODO: use ir_data
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
