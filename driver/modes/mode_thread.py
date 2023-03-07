from driver.modes.mode import Mode


class ModeThread:
    def __init__(self, mode: Mode):
        self._mode = mode

    def start(self):
        pass

    def stop(self):
        pass

    def _loop(self):
        pass