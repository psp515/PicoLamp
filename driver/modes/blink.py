import globals
from device import Device
from device_state import DeviceState
from enums.mode_state_enum import ModeStateEnum
from globals import OFF_COLOR, MINIMUM_BLINK_SPAN
from modes.mode import Mode
from time import ticks_ms, ticks_diff, ticks_add


class Blink(Mode):
    def __init__(self, device: Device, device_state: DeviceState, colors=None, speed=None):
        super().__init__(device, device_state)
        if colors == None:
            colors = globals.DEVICE_COLORS
        self.colors = [tuple(x) for x in colors]
        self.speed = MINIMUM_BLINK_SPAN if speed is None else max(speed, MINIMUM_BLINK_SPAN)
        self.color = self.colors[0]
        self._next = ticks_add(ticks_ms(), self.speed)
        self._is_shining = False

    def loop(self):
        if self.state == ModeStateEnum.OFF:
            return

        current = ticks_ms()

        if ticks_diff(current, self._next) >= 0:
            if self._is_shining:
                self._write_color(OFF_COLOR.rgb_color)
                self._is_shining = False
            else:
                self.color = self.colors[current % len(self.colors)]
                self._write_color(self.color)
                self._is_shining = True
            self._next = ticks_add(ticks_ms(), self.speed)

    def start(self):
        self._write_color(OFF_COLOR.rgb_color)
        self._next = ticks_add(ticks_ms(), self.speed)
        self._is_shining = False
        self.state = ModeStateEnum.ON

    def update(self, json):
        if json is not None:
            if "speed" in json:
                self.speed = max(json["speed"], MINIMUM_BLINK_SPAN)
            if "colors" in json:
                tmp_colors = json["colors"]
                if len(tmp_colors) > 0:
                    self.colors = [tuple(x) for x in tmp_colors]

        self.state = ModeStateEnum.ON

    def refresh_led(self):
        if not self._is_shining:
            return
        self._write_color(self.color)
        self.state = ModeStateEnum.ON

    def end(self):
        self._write_color(OFF_COLOR.rgb_color)
        self.state = ModeStateEnum.OFF

    def _write_color(self, to_color):
        current_color = self._calc_color(to_color)
        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            for led in group:
                self._device.strip[led] = current_color if state else OFF_COLOR.rgb_color
        self._device.strip.write()

    def _calc_color(self, color):
        return tuple([int(self._desired_state.brightness * x) for x in color])


