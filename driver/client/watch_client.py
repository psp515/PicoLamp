from device_state import DeviceState
from tools.blink_logger import Logger


class WatchClient:
    def __init__(self, device_state: DeviceState, logger: Logger):
        self._logger = logger
        self._device_state = device_state
        self._topics = {}

    def watch_topic(self, topic, callback):
        self._topics[topic] = callback
