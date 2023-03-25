from umqtt.simple import MQTTClient

from client.watch_client import WatchClient
from device_state import DeviceState
from tools.logger import Logger
from enums.logger_enum import LoggerEnum


class HivemqMQTTClient(WatchClient):
    client: MQTTClient
    _data = {}

    def __init__(self, data, logger: Logger, device_state: DeviceState):
        super().__init__(device_state, logger)
        self._data = data

        self.client = self.client = MQTTClient(
            client_id=self._data["client_id"],
            server=self._data["server"],
            port=self._data["port"],
            user=self._data["user"],
            password=self._data["password"],
            keepalive=self._data["keepalive"],
            ssl=self._data["ssl"],
            ssl_params={"server_hostname": str(data["ssl_params_server_hostname"])})

        self.client.set_callback(self._callback)

    def connect(self):
        self.client.connect()

    def _callback(self, topic, data):
        topic = topic.decode("utf-8")
        data = data.decode("utf-8")

        if topic not in self._topics:
            self._logger.log(f"{topic} not found in topics.", LoggerEnum.WARNING)
            return

        self._logger.log(f"Data from topic '{topic}' received.", LoggerEnum.INFO)
        self._topics[topic](data, self._device_state, self._logger)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def subscribe(self, topic):
        self.client.subscribe(topic)
