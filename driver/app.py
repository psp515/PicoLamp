from network import WLAN
from utime import sleep

from client.hivemq_client import HivemqMQTTClient
from device import Device
from device_management import mqtt_state, mqtt_mode
from device_state import DeviceState
from modes.mode_thread import ModeThread
from tools.logger import Logger
from enums.logger_enum import LoggerEnum


class App:
    device: Device
    logger: Logger
    client: HivemqMQTTClient
    wlan: WLAN
    device_state: DeviceState

    def __init__(self,
                 device: Device,
                 device_state: DeviceState,
                 logger: Logger,
                 client: HivemqMQTTClient,
                 wlan: WLAN,
                 colors: []):
        self.colors = colors
        self.device_state = device_state
        self.wlan = wlan
        self.client = client
        self.logger = logger
        self.device = device
        self.mode_thread = ModeThread(device, device_state)

    def start(self):
        # TODO: add states, get like get config

        topics = ["state", "mode"]
        mqtt = [("state", mqtt_state), ("mode", mqtt_mode)]

        for topic, func in mqtt:
            self.client.watch_topic(topic, func)

        #TODO: add ir topics

        self.mode_thread.start()

        while True:
            if self.wlan.isconnected():
                for topic in topics:
                    self.client.subscribe(topic)

                if self.device_state.push_device_state:
                    # TODO: publish data with mqtt
                    pass
            else:
                self.logger.log("Device disconnected from internet.", LoggerEnum.WARNING)
                sleep(1)
