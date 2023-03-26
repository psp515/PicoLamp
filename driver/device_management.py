from ujson import loads

from client.hivemq_client import HivemqMQTTClient
from client.nec_client import NECClient
from device_state import DeviceState
from enums.device_state_enum import DeviceStateEnum
from enums.logger_enum import LoggerEnum
from tools.ir_rx_message import IRReceiveMessage
from tools.logger import Logger


def configure_mqtt(client: HivemqMQTTClient):
    mqtt = [("state", mqtt_state),
            ("mode", mqtt_mode),
            ("ping", mqtt_ping),
            ("update_mode", mqtt_update_mode)]

    for topic, func in mqtt:
        client.watch_topic(topic, func)

    return [x[0] for x in mqtt]


def configure_ir(client: NECClient, data_to_map: {}):
    mapper = [("ON", ir_on), ("OFF", ir_off), ("BUP", ir_bright_up), ("BDOWN", ir_bright_down), ("MLED", ir_more_led),
              ("LLED", ir_less_led), ("NCOLOR", ir_next_color), ("PCOLOR", ir_prev_color), ("M1", ir_mode_1),
              ("M2", ir_mode_2), ("M3", ir_mode_3), ("M4", ir_mode_4), ("M5", ir_mode_5), ("M6", ir_mode_6),
              ("M7", ir_mode_7), ("M8", ir_mode_8)]

    ir = [(data_to_map[x[0]], x[1]) for x in mapper]

    for topic, func in ir:
        client.watch_topic(topic, func)


def mqtt_state(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

    if data["state"] == 0 and device_state.state == DeviceStateEnum.ON:
        device_state.state = DeviceStateEnum.OFF
    elif data["state"] == 1 and device_state.state == DeviceStateEnum.OFF:
        device_state.state = DeviceStateEnum.STARTING


def mqtt_update_mode(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

    if device_state.state == DeviceStateEnum.OFF:
        return

    binary_data = data["groups_state"]
    device_state.groups_state = [bool(bit) for bit in binary_data]
    device_state.old_brightness = device_state.brightness
    device_state.brightness = data["brightness"]
    device_state.state = DeviceStateEnum.UPDATE

    if "extend" in data:
        device_state.update_json = data["extend"]
        device_state.state = DeviceStateEnum.EXTENDED_UPDATE


def mqtt_led(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)


def mqtt_mode(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)


def mqtt_ping(json: str, device_state: DeviceState, logger: Logger):
    logger.log(f"Ping.\n{json}", LoggerEnum.INFO)


def ir_on(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    if device_state.state == DeviceStateEnum.OFF:
        device_state.state = DeviceStateEnum.ON


def ir_off(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    if device_state.state == DeviceStateEnum.ON:
        device_state.state = DeviceStateEnum.OFF


def ir_more_led(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_less_led(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_bright_up(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_bright_down(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_next_color(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_prev_color(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_mode_1(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_mode_2(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_mode_3(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_mode_4(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_mode_5(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_mode_6(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_mode_7(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass


def ir_mode_8(device_state: DeviceState, logger: Logger, message: IRReceiveMessage):
    pass
