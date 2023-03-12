from ujson import loads
from device_state import DeviceState
from enums.device_state_enum import DeviceStateEnum
from tools.logger import Logger


def mqtt_state(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

    if data["state"] == 0 and device_state.is_working:
        device_state.status = DeviceStateEnum.OFF
    elif data["state"] == 1 and not device_state.is_working:
        device_state.is_working = DeviceStateEnum.ON


def mqtt_mode(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)
