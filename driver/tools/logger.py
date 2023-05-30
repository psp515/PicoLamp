from enums.logger_enum import LoggerEnum


class Logger:
    def __init__(self, debug: bool):
        self.debug = debug

    def log(self, message: str, information: LoggerEnum):
        actions = self.get_information_data(information)
        print(f"Debug: {self.debug} - {actions[0]} - {actions[1]}: {message}")

    @staticmethod
    def get_information_data(information: LoggerEnum):
        if information == LoggerEnum.INFO:
            return 0, "INFO"
        elif information == LoggerEnum.WARNING:
            return 1, "WARNING"
        elif information == LoggerEnum.ERROR:
            return 2, "ERROR"
        elif information == LoggerEnum.SETUP_ERROR:
            return 3, "SETUP ERROR"
        elif information == LoggerEnum.CONNECTION_ERROR:
            return 4, "CONNECTION ERROR"

        return 0, "DEBUG"
