from ujson import loads
from device_state import DeviceState
from enums.device_state_enum import DeviceStateEnum
from enums.logger_enum import LoggerEnum
from tools.logger import Logger


def mqtt_state(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

    if data["state"] == 0 and device_state.state == DeviceStateEnum.ON:
        device_state.state = DeviceStateEnum.OFF
    elif data["state"] == 1 and device_state.state == DeviceStateEnum.OFF:
        device_state.state = DeviceStateEnum.STARTING


def mqtt_mode(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

def mqtt_ping(json: str, device_state: DeviceState, logger: Logger):
    logger.log(f"Ping.\n{json}", LoggerEnum.INFO)