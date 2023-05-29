from ujson import loads

from client.hivemq_client import HivemqMQTTClient
from client.nec_client import NECClient
from device_state import DeviceState
from enums.device_state_enum import DeviceStateEnum
from enums.logger_enum import LoggerEnum
from tools.blink_logger import Logger


def configure_mqtt(client: HivemqMQTTClient):
    mqtt = [("state", mqtt_state),
            ("ping", mqtt_ping),
            ("update_mode", mqtt_update_mode),
            ("new_mode", mqtt_new_mode),
            ("update_led", mqtt_update_led)]

    for topic, func in mqtt:
        client.watch_topic(topic, func)

    return [x[0] for x in mqtt]


def mqtt_ping(json: str, device_state: DeviceState, logger: Logger):
    logger.log(f"Ping.\n{json}", LoggerEnum.INFO)


def mqtt_state(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

    if data["state"] == 0 and device_state.state == DeviceStateEnum.ON:
        device_state.state = DeviceStateEnum.ENDING
        logger.log("Switching device off.", LoggerEnum.DEBUG)
    elif data["state"] == 1 and device_state.state == DeviceStateEnum.OFF:
        device_state.state = DeviceStateEnum.STARTING
        logger.log("Switching device on.", LoggerEnum.DEBUG)


def mqtt_update_mode(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

    if device_state.state == DeviceStateEnum.OFF:
        logger.log("Device is off no action taken.", LoggerEnum.DEBUG)
        return

    device_state.old_brightness = device_state.brightness
    
    if "brightness" in data:
        device_state.brightness_prev = device_state.brightness
        device_state.brightness = data["brightness"]

    if "extend" in data:
        device_state.json = data["extend"]

    device_state.state = DeviceStateEnum.UPDATE


def mqtt_update_led(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

    if device_state.state == DeviceStateEnum.OFF:
        logger.log("Device is off no action taken.", LoggerEnum.DEBUG)
        return

    binary_data = data["states"]
    device_state.groups_state = [bool(bit) for bit in binary_data]

    device_state.state = DeviceStateEnum.LED_UPDATE


def mqtt_new_mode(json: str, device_state: DeviceState, logger: Logger):
    data = loads(json)

    if device_state.state == DeviceStateEnum.OFF:
        logger.log("Device is off no action taken.", LoggerEnum.DEBUG)
        return

    device_state.mode = data["mode"]
    data = data["data"]
     
    if "brightness" in data:
        device_state.brightness_prev = device_state.brightness
        device_state.brightness = data["brightness"]

    if "extend" in data:
        device_state.json = data["extend"]

    device_state.state = DeviceStateEnum.NEW


def configure_ir(client: NECClient, data_to_map: {}):
    """mapper = [("ON", ir_on), ("OFF", ir_off), ("BUP", ir_bright_up), ("BDOWN", ir_bright_down),
                ("MLED", ir_more_led),
                ("LLED", ir_less_led), ("NCOLOR", ir_next_color), ("PCOLOR", ir_prev_color), ("M1", ir_mode_1),
                ("M2", ir_mode_2), ("M3", ir_mode_3), ("M4", ir_mode_4), ("M5", ir_mode_5), ("M6", ir_mode_6),
                ("M7", ir_mode_7), ("M8", ir_mode_8)]

    ir = [(data_to_map[x[0]], x[1]) for x in mapper]

    for topic, func in ir:
        client.watch_topic(topic, func) """
    pass
