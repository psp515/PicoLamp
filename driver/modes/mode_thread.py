from driver.modes.mode import Mode


class ModeThread:

    _mode: Mode

    def __init__(self, mode: Mode):
        self._mode = mode
        self._is_running = False

    def start(self):
        _mode.on()

    def stop(self):
        pass

    def _loop(self):
        pass