from device import Device
from device_state import DeviceState
from globals import DEFAULT_COLOR, OFF_COLOR
from models.color import Color
from modes.mode import Mode


class ConstantColorNA(Mode):
    def __init__(self, device: Device, device_state: DeviceState, color: Color = DEFAULT_COLOR):
        super().__init__(device, device_state)
        self.color = color.rgb_color

    def loop(self):
        pass

    def start(self):
        self._write_color(self.color)

    def update(self):
        self._write_color(self.color)

    def extended_update(self, json):
        self.color = tuple(json["color"])
        self._write_color(self.color)

    def refresh_led(self):
        self._write_color(self.color)

    def end(self):
        self._write_color(OFF_COLOR.rgb_color)

    def _write_color(self, to_color):
        current_color = self._calc_color(to_color)
        for group, state in zip(self._device.np_groups, self._device_state.groups_state):
            for led_id in group:
                self._device.strip[led_id] = current_color if state else OFF_COLOR.rgb_color
        self._device.strip.write()

    def _calc_color(self, color):
        return tuple([int(self._device_state.brightness * x) for x in color])
