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


def ir_on(device_state: DeviceState, logger: Logger):
    pass


def ir_off(device_state: DeviceState, logger: Logger):
    pass


def ir_more_led(device_state: DeviceState, logger: Logger):
    pass


def ir_less_led(device_state: DeviceState, logger: Logger):
    pass


def ir_bright_up(device_state: DeviceState, logger: Logger):
    pass


def ir_bright_down(device_state: DeviceState, logger: Logger):
    pass


def ir_next_color(device_state: DeviceState, logger: Logger):
    pass


def ir_prev_color(device_state: DeviceState, logger: Logger):
    pass


def ir_mode_1(device_state: DeviceState, logger: Logger):
    pass


def ir_mode_2(device_state: DeviceState, logger: Logger):
    pass


def ir_mode_3(device_state: DeviceState, logger: Logger):
    pass


def ir_mode_4(device_state: DeviceState, logger: Logger):
    pass


def ir_mode_5(device_state: DeviceState, logger: Logger):
    pass


def ir_mode_6(device_state: DeviceState, logger: Logger):
    pass


def ir_mode_7(device_state: DeviceState, logger: Logger):
    pass
