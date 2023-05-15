import _thread

from network import WLAN
from utime import sleep, ticks_ms, ticks_diff
from machine import Timer

from client.hivemq_client import HivemqMQTTClient
from client.nec_client import NECClient
from device import Device
from device_state import DeviceState
from modes.mode_thread import ModeThread
from tools.logger import Logger
from enums.logger_enum import LoggerEnum
from enums.subdevice_state import SubdeviceState

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
                 mqtt_topics: [],
                 nec_client: NECClient,
                 wlan: WLAN):
        self.device_state = device_state
        self.wlan = wlan
        self.client = client
        self.nec_client = nec_client
        self.logger = logger
        self.device = device
        self.mode_thread = ModeThread(device, device_state, wlan, logger)
        self.topics = mqtt_topics

    def start(self):
        _thread.start_new_thread(self.mode_thread.loop, ())
        self.logger.log("Receiver thread starting.", LoggerEnum.INFO)

        while True:

            if self.wlan.isconnected():
                for topic in self.topics:
                    self.client.subscribe(topic)

                if self.device_state.push_device_state:
                    # TODO: publish data with mqtt
                    pass
            else:
                self.logger.log("Device disconnected from internet.", LoggerEnum.WARNING)
                sleep(1)