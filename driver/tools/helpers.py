from utime import sleep
from enums.logger_enum import LoggerEnum
from exception.setup_error import SetupError
import network

from exception.setup_error import SetupError

def generate_groups(sizes: [], total_length: int):
    groups = []
    length = 0

    if len(sizes) == 0:
        SetupError("Invalid number of groups.")

    for size in sizes:
        groups.append([length + i for i in range(size)])
        length += size

    if length != total_length:
        SetupError("Invalid number of led-s in groups.")

    return groups


def validate_strip_config(config: {}, used_pins: []):
    if config["pin"] is None or config["pin"] in used_pins:
        raise SetupError("Invalid strip config. (No pin or pin is used)")

    used_pins.append(config["pin"])

    if config["size"] is None:
        raise SetupError("Invalid strip config. (No size)")

    if config["groups"] is None:
        raise SetupError("Invalid strip config. (No groups)")


def validate_ir_config(config: {}, used_pins: []):
    if config["pin"] is None or config["pin"] in used_pins:
        raise SetupError("Invalid strip config. (No pin or pin is used)")

    for name in ["ON", "OFF", "BUP", "BDOWN", "MLED", "LLED", "NCOLOR", "PCOLOR",
                 "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]:
        if config[name] is None:
            raise SetupError(f"Invalid ir config. (lack of {name})")


def validate_wlan_config(config: {}):
    if config["ssid"] is None:
        raise SetupError("Invalid wlan config. (No ssid)")

    if config["password"] is None:
        raise SetupError("Invalid wlan config. (No password)")


def validate_hivemq_config(config: {}):
    for name in ["client_id", "server", "port", "user",
                 "password", "keepalive", "ssl", "ssl_params_server_hostname"]:
        if config[name] is None:
            raise SetupError(f"Invalid hivemq config. (lack of {name})")


def wait_for_connection(wifi: network.WLAN, logger: Logger):
    sleep(1)
    i = 0
    while not wifi.isconnected() and i < 10:
        logger.log(f"Not Connected. Status: {wifi.status()}. Awaiting.", LoggerEnum.WARNING)
        i += 1
        sleep(1)

    if not wifi.isconnected():
        logger.log(f"Not Connected. Status: {wifi.status()}. ", LoggerEnum.WARNING)
        raise SetupError("Not connected to the internet.")

