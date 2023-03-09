from network import WLAN

from client.hivemq_client import HivemqMQTTClient
from device import Device
from device_state import DeviceState
from modes.mode_thread import ModeThread
from tools.logger import Logger


class App:
    device: Device
    logger: Logger
    client: HivemqMQTTClient
    wlan: WLAN
    topics: []

    def __init__(self,
                 device: Device,
                 logger: Logger,
                 client: HivemqMQTTClient,
                 wlan: WLAN,
                 topics: []):
        self.wlan = wlan
        self.client = client
        self.logger = logger
        self.device = device
        self.topics = topics

    def mqtt_state(self, json, device_state: DeviceState):
        pass

    def mqtt_mode(self):
        pass

    def ir_state(self):
        pass

    def ir_mode(self):
        pass

    def start(self):



        mode_thread = ModeThread()
        ModeThread.start()

        while True:
            if self.wlan.isconnected():
                for topic in self.topics:
                    self.client.subscribe(topic)

                if self.device.un_pushed_changes:
                    # TODO
                    # publish data with mqtt
                    # on topics but with '_device' signature ??
                    pass
            else:
                self.logger.log("Device disconnected from internet.", LoggerEnum.WARNING)
                sleep(1)
