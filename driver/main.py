from machine import Pin, reset
from neopixel import NeoPixel

from app import App
from utime import sleep

import gc
import network

from client.hivemq_client import HivemqMQTTClient
from client.nec_client import NECClient
from device import Device
from device_management import configure_mqtt, configure_ir
from device_state import DeviceState
from exception.setup_error import SetupError
from subdevices.nec_receiver.nec_receiver import NECReceiver
from tools.helpers import generate_groups, validate_strip_config, validate_ir_config, validate_wlan_config, \
    validate_hivemq_config
from tools.logger import Logger
from enums.logger_enum import LoggerEnum
from tools.config_readers import read_json, read_colors
import globals


def wait_for_connection(wifi: network.WLAN):
    sleep(1)
    i = 0
    while not wifi.isconnected() and i < 10:
        logger.log(f"Not Connected. Status: {wifi.status()}. Awaiting.", LoggerEnum.WARNING)
        i += 1
        sleep(1)

    if not wlan.isconnected():
        logger.log(f"Not Connected. Status: {wlan.status()}. ", LoggerEnum.WARNING)


if __name__ == '__main__':
    gc.collect()
    used_pins = [25]
    led = Pin("LED", Pin.OUT)
    led.low()
    logger = Logger(led)
    logger.log("Logger is working!", LoggerEnum.INFO)

    try:
        # Others
        globals.device_colors = read_colors("config/colors.json")

        if len(globals.device_colors) < 1:
            raise SetupError("Invalid colors config. Should contain at least 1 color.")

        # Device

        strip_conf = read_json("config/strip.json")
        validate_strip_config(strip_conf, used_pins)

        neopixel_pin = Pin(strip_conf["pin"])
        neopixel = NeoPixel(neopixel_pin, strip_conf["size"])
        device_state = DeviceState(strip_conf["size"])
        groups = generate_groups(strip_conf["groups"], strip_conf["size"])

        ir_config = read_json("config/pilot.json")
        validate_ir_config(ir_config, used_pins)
        nec_receiver = NECReceiver(ir_config["pin"])

        device = Device(neopixel, groups, nec_receiver)

        # WIFI

        wlan_config = read_json("config/secrets.json")
        validate_wlan_config(wlan_config)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(wlan_config["ssid"], wlan_config["password"])
        wait_for_connection(wlan)

        # HiveMQ Client

        hivemq_config = read_json("config/hivemq.json")
        validate_hivemq_config(hivemq_config)
        mqtt_client = HivemqMQTTClient(hivemq_config, logger, device_state)
        mqtt_client.connect()
        mqtt_topics = configure_mqtt(mqtt_client)

        # NEC Client

        nec_client = NECClient(nec_receiver, device_state, logger)
        configure_ir(nec_client, ir_config)

        # Starting app

        app = App(device, device_state, logger, mqtt_client, mqtt_topics, nec_client, wlan)
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
