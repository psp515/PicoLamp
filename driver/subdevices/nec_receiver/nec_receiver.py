from machine import Timer, Pin
from utime import ticks_us, ticks_diff

from enums.receiver_enum import ReceiveState
from enums.subdevice_state import SubdeviceState
from tools.ir_rx_message import IRReceiveMessage


BITS = 32 + 2
PULSES = BITS * 2
REPEAT_PULSES = 4

TRIGGER_TIME_MS = 70

START_MIN_ONE_BIT_US = 6000
START_MIN_ZERO_BIT_US = 2500
START_MAX_REPEAT_ZERO_BIT_US = 2500

REPEAT_US = 2500

# 562.5 us 1 state and 562.5 us 0 state
ZERO_BIT_US = 1125

# 562.5 us 1 state and 1687.5 us 0 state
ONE_BIT_US = 2250


class NECReceiver:
    def __init__(self, pin: int):
        self._initialized_pin = Pin(pin, Pin.IN)
        self._initialized_pin.irq(trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), handler=self._trigger_callback)
        self.pulses = []
        self.timer = Timer(-1)
        self._callback = None
        self.state = SubdeviceState.ON
        self._last_command = -1
        self._last_address = -1

    def _trigger_callback(self, pin):
        try:
            pulse = ticks_us()

            if self.state is SubdeviceState.BUSY:
                self.pulses.append(pulse)
                if len(self.pulses) > 2 * PULSES:
                    print("Clear")
                    self._parse_data(None)
                return
        
            self.state = SubdeviceState.BUSY
            self.timer.init(mode=Timer.ONE_SHOT, period=TRIGGER_TIME_MS, callback=self._parse_data)
            self.pulses = [pulse]
        except Exception as e:
            print("Error", e)

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, callback):
        self._callback = callback

    def _parse_data(self, timer):

        message = None
        pulses_count = len(self.pulses)
        try:
            if pulses_count > PULSES:
                raise RuntimeError(ReceiveState.OVERRUN)
            
            if pulses_count < 3:
                raise RuntimeError(ReceiveState.BAD_START)
            
            start_one_width = ticks_diff(self.pulses[1], self.pulses[0])

            if start_one_width < START_MIN_ONE_BIT_US:
                raise RuntimeError(ReceiveState.BAD_START)

            start_zero_width = ticks_diff(self.pulses[2], self.pulses[1])

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

                address = self._get_byte(3, 19, self.pulses)
                address_complement = self._get_byte(19, 35, self.pulses)
                command = self._get_byte(35, 51, self.pulses)
                command_complement = self._get_byte(51, 66, self.pulses)

                if address & address_complement != 0:
                    raise RuntimeError(ReceiveState.BAD_ADDRESS)

                if command & command_complement != 0:
                    raise RuntimeError(ReceiveState.BAD_DATA)

                self._last_command = command
                self._last_address = address

                message = IRReceiveMessage(ReceiveState.OK, command, address)
        except RuntimeError as e:
            message = IRReceiveMessage(e.args[0])

        self.state = SubdeviceState.ON
        self.pulses = []
        self.callback(message)

    def _get_byte(self, start: int, stop: int, array: []):
        value = 0

        for i in range(start, stop, 2):
            value >>= 1
            if ticks_diff(array[i+1], array[i]) > ZERO_BIT_US:
                value |= 0x80

        return value