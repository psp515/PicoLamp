from client.watch_client import WatchClient
from device_state import DeviceState
from enums.logger_enum import LoggerEnum
from subdevices.nec_receiver.nec_receiver import NECReceiver
from tools.ir_rx_message import IRReceiveMessage
from tools.blink_logger import Logger


class NECClient(WatchClient):
    def __init__(self, nec_receiver: NECReceiver, device_state: DeviceState, logger: Logger):
        super().__init__(device_state, logger)
        self.nec_ir = nec_receiver
        self.nec_ir.callback = self._callback
    
    def _callback(self, message: IRReceiveMessage):
        if not message.is_succesfull:
            return

        if message.command not in self._topics:
            self._logger.log(f"{message.command} not found in topics.", LoggerEnum.ERROR)
            return

        self._logger.log(f"Recived command: {message.command}.", LoggerEnum.INFO)
        self._topics[message.command](self._device_state, self._logger, message)
