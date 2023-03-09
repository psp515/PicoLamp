from umqtt.simple import MQTTClient
from utime import sleep
from machine import reset
from device import Device
from tools.logger import Logger
from tools.logger_enum import LoggerEnum

class HivemqMQTTClient:
    client: MQTTClient
    _data = {}

    def __init__(self, data, logger: Logger, device: Device):
        self._logger = logger
        self._device = device
        self._data = data

        self.client = self.client = MQTTClient(
            client_id=self._data["client_id"],
            server=self._data["server"],
            port=self._data["port"],
            user=self._data["user"],
            password=self._data["password"],
            keepalive=self._data["keepalive"],
            ssl=self._data["ssl"],
            ssl_params={"server_hostname" :str(data["ssl_params"]["server_hostname"])})

        self.client.set_callback(self._callback)
        self._topics = {}

    def connect(self):
        self.client.connect()

    def _callback(self, topic, data):
        topic = topic.decode("utf-8")
        data = data.decode("utf-8")

        print(topic, data)

        if topic not in self._topics:
            self._logger.log(f"{topic} not found in topics.", LoggerEnum.WARNING)
            return

        self._topics[topic](data, self._device, self._logger)

    def watch_topic(self, topic, callback):
        self._topics[topic] = callback

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def subscribe(self, topic):
        self.client.subscribe(topic)
