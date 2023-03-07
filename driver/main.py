from machine import Pin, UART, reset
from app import App

import gc

from driver.tools.logger import Logger
from driver.tools.logger_enum import LoggerEnum

if __name__ == '__main__':
    gc.collect()

    uart = UART(0, tx=Pin(0), rx=Pin(1))
    led = Pin("LED", Pin.OUT)
    led.low()
    logger = Logger(led, uart)

    try:

        # TODO initialize elements
        # TODO connect to wifi
        # TODO connect to mqtt client

        app = App()

        app.start()
    except OSError as e:
        logger.log(e, LoggerEnum.CONNECTION_ERROR)
    except Exception as e:
        logger.log(e, LoggerEnum.ERROR)
    finally:
        reset()
