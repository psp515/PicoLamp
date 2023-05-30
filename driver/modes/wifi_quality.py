from device import Device
from device_state import DeviceState
from modes.animated_mode import AnimatedMode
from enums.mode_state_enum import ModeStateEnum
from globals import OFF_COLOR, EXCELLENT_CONNECTION, GOOD_CONNECTION, POOR_CONNECTION, \
    BAD_CONNECTION, UNRESOLVED_CONNECTION
from tools.config_readers import read_json


class WifiQuality(AnimatedMode):

    def __init__(self, device: Device, desired_state: DeviceState):
        super().__init__(device, desired_state)
        self.brightness = desired_state.brightness
        self._itr = 0
        self._max = desired_state.speed
        self._strip_colors = [device.strip[i] for i in range(len(device.strip))]
        self.prev_color = None
        self.color = UNRESOLVED_CONNECTION
        wlan_config = read_json("config/secrets.json")
        self._wlan_name = wlan_config["ssid"]

    def end(self):
        self.state = ModeStateEnum.ENDING
        self._default()

    def end_step(self):
        self._itr += 1
        self._animate(OFF_COLOR.rgb_color)
        if self._itr == self._max:
            self.state = ModeStateEnum.OFF

    def start(self):
        self.state = ModeStateEnum.STARTING
        self._default()

    def start_step(self):
        self._itr += 1
        self._animate(self.color)
        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self.color = self._check_connection()
            self._itr = 0
            self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def step(self):
        self._itr += 1

        if self.color != self.prev_color:
            self._animate(self.color)

        if self._itr == self._max:
            self.state = ModeStateEnum.ON
            self.prev_color = self.color
            self.color = self._check_connection()
            self._itr = 0
            self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def update(self, json):
        self.state = ModeStateEnum.UPDATING
        self._default()

    def update_step(self):
        self._itr += 1

        self._animate(self.color)
        if self._itr == self._max:
            self.state = ModeStateEnum.ON

    def _default(self):
        self._itr = 0
        self._max = self._desired_state.speed
        self._strip_colors = [self._device.strip[i] for i in range(len(self._device.strip))]

    def refresh_led(self):
        if self._itr == 0:
            for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
                for led in group:
                    if state:
                        self._device.strip[led] = self._calc_color(self.color)
                    else:
                        self._device.strip[led] = OFF_COLOR.rgb_color

    def _animate(self, to_color: ()):
        n = self._desired_state.speed
        rising, downing = self._itr / n, (n - self._itr) / n

        if self._desired_state.brightness_prev == self._desired_state.brightness:
            bright = self._desired_state.brightness
        else:
            bright = (rising * self._desired_state.brightness + downing * self._desired_state.brightness_prev)

        for group, state in zip(self._device.np_groups, self._desired_state.groups_state):
            if state:
                for led in group:
                    led_prev = self._strip_colors[led]
                    color = tuple([int(downing * led_prev[i] + rising * to_color[i] * bright) for i in range(3)])
                    self._device.strip[led] = color

        self._device.strip.write()

    def _calc_color(self, color):
        return tuple([int(self._desired_state.brightness * x) for x in color])

    def _check_connection(self):
        ap_list = self._desired_state.wifi

        if len(ap_list) == 0:
            return UNRESOLVED_CONNECTION

        for ap in ap_list:
            if ap[0].decode() == self._wlan_name:
                if ap[3] >= -50:
                    return EXCELLENT_CONNECTION
                elif ap[3] >= -60:
                    return GOOD_CONNECTION
                elif ap[3] >= -70:
                    return POOR_CONNECTION
                else:
                    return BAD_CONNECTION

        return UNRESOLVED_CONNECTION
