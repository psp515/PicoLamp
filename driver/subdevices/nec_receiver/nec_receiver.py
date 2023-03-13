from machine import Timer, Pin
from utime import ticks_us, ticks_diff

from const import TRIGGER_TIME_MS, START_MIN_ONE_BIT_US, PULSES, START_MAX_REPEAT_ZERO_BIT_US, REPEAT_PULSES, \
    ZERO_BIT_US
from device_state import DeviceState
from enums.receiver_enum import ReceiveState
from enums.subdevice_state import SubdeviceState
from tools.ir_rx_message import IRReceiveMessage
from tools.logger import Logger


class NECReceiver:
    def __init__(self, device_state: DeviceState,
                 logger: Logger,
                 pin: int):
        self.logger = logger
        self.device_state = device_state
        self._initialized_pin = Pin(pin, Pin.IN)
        self._initialized_pin.irq(trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), handler=self._trigger_callback)
        self._pulses = []
        self._timer = Timer(-1)
        self._callback = None
        self._state = SubdeviceState.ON

    def _trigger_callback(self):
        pulse = ticks_us()

        if self._state is SubdeviceState.BUSY:
            self._pulses.append(pulse)
            return

        self._state = SubdeviceState.BUSY
        self._timer.init(mode=Timer.ONE_SHOT, period=TRIGGER_TIME_MS, callback=self._parse_data)
        self._pulses = [pulse]

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, callback):
        self._callback = callback

    def _parse_data(self, timer):
        message = None
        pulses_count = len(self._pulses)
        try:
            if pulses_count > PULSES:
                raise RuntimeError(ReceiveState.OVERRUN)

            start_one_width = ticks_diff(self._pulses[1], self._pulses[0])

            if start_one_width < START_MIN_ONE_BIT_US:
                raise RuntimeError(ReceiveState.BAD_START)

            start_zero_width = ticks_diff(self._pulses[2], self._pulses[1])

            if start_zero_width < START_MAX_REPEAT_ZERO_BIT_US:

                if pulses_count > REPEAT_PULSES:
                    raise RuntimeError(ReceiveState.BAD_START)

                if self._last_command == -1:
                    raise RuntimeError(ReceiveState.BAD_LAST_DATA)

                if self._last_address == -1:
                    raise RuntimeError(ReceiveState.BAD_LAST_ADDRESS)

                message = IRReceiveMessage(ReceiveState.REPEAT, self._last_command, self._last_address)
            else:
                if start_zero_width < START_MAX_REPEAT_ZERO_BIT_US and PULSES == pulses_count:
                    raise RuntimeError(ReceiveState.BAD_START)
                elif start_zero_width > START_MAX_REPEAT_ZERO_BIT_US and pulses_count < PULSES:
                    raise RuntimeError(ReceiveState.BAD_BLOCK)

                address = self._get_byte(3, 19, self._pulses)
                address_complement = self._get_byte(19, 35, self._pulses)
                command = self._get_byte(35, 51, self._pulses)
                command_complement = self._get_byte(51, 66, self._pulses)

                if address & address_complement != 0:
                    raise RuntimeError(ReceiveState.BAD_ADDRESS)

                if command & command_complement != 0:
                    raise RuntimeError(ReceiveState.BAD_DATA)

                self._last_command = command
                self._last_address = address

                message = IRReceiveMessage(ReceiveState.OK, command, address)
        except RuntimeError as e:
            message = IRReceiveMessage(e.args[0])

        self._state = SubdeviceState.ON
        self.callback(self.device_state, self.logger, message)

    def _get_byte(self, start: int, stop: int, array: []):
        value = 0

        for i in range(start, stop, 2):
            value >>= 1
            if ticks_diff(array[i+1], array[i]) > ZERO_BIT_US:
                value |= 0x80

        return value
