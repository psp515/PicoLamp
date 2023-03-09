

class DeviceState:
    """Class purpose is to represent state of the device"""
    def __init__(self, n_of_groups):
        self.brightness = 1
        self.groups_state = [True] * n_of_groups
        self.change_mode = False
        self.new_mode = None # ENUM??
        self.new_mode_additional_data = None
        self.is_on = False
        self.update_mode = False
        self.update_json = None
