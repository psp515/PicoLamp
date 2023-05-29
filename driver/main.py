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
from tools.logger import Logger
from tools.initialization_helpers import generate_groups, validate_strip_config, validate_ir_config, validate_wlan_config, \
    validate_hivemq_config, wait_for_connection
from tools.blink_logger import BlinkLogger
from enums.logger_enum import LoggerEnum
from tools.config_readers import read_json, read_colors
import globals

DEBUG = True

if __name__ == '__main__':
    gc.collect()
    logger = Logger(DEBUG)

    try:
        # BlinkLogger
        used_pins = [25]
        led = Pin("LED", Pin.OUT)
        led.low()
        logger = BlinkLogger(led, DEBUG)
        logger.log("Logger is working!", LoggerEnum.INFO)

        # Others
        logger.log("Other init start.", LoggerEnum.INFO)

        globals.DEVICE_COLORS = read_colors("config/colors.json")
        if len(globals.DEVICE_COLORS) < 2:
            raise SetupError("Invalid colors config. Should contain at least 2 colors.")

        logger.log("Other init finished.", LoggerEnum.INFO)

        # Device
        logger.log("Device init start.", LoggerEnum.INFO)

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

        logger.log("Device init finished.", LoggerEnum.INFO)
        # WIFI
        logger.log("WIFI init start.", LoggerEnum.INFO)

        wlan_config = read_json("config/secrets.json")
        validate_wlan_config(wlan_config)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(wlan_config["ssid"], wlan_config["password"])
        wait_for_connection(wlan, logger)

        logger.log("WIFI init finished.", LoggerEnum.INFO)
        # HiveMQ Client
        logger.log("HiveMQ init start.", LoggerEnum.INFO)

        hivemq_config = read_json("config/hivemq.json")
        validate_hivemq_config(hivemq_config)
        mqtt_client = HivemqMQTTClient(hivemq_config, logger, device_state)
        mqtt_client.connect()
        mqtt_topics = configure_mqtt(mqtt_client)

        logger.log("HiveMQ init finished.", LoggerEnum.INFO)
        # NEC Client
        logger.log("NEC init start.", LoggerEnum.INFO)

        nec_client = NECClient(nec_receiver, device_state, logger)
        configure_ir(nec_client, ir_config)
        device_state.ir = nec_receiver

        logger.log("NEC init finished.", LoggerEnum.INFO)
        # Starting app

        app = App(device, device_state, logger, mqtt_client, mqtt_topics, nec_client, wlan)
        logger.log("App starting!", LoggerEnum.INFO)
        app.start()
    except OSError as e:
        logger.log(str(e), LoggerEnum.CONNECTION_ERROR)
    except SetupError as e:
        logger.log(str(e), LoggerEnum.SETUP_ERROR)
    except BaseException as e:
        logger.log(str(e), LoggerEnum.ERROR)
    finally:
        if not DEBUG:
            sleep(3)
            reset()
