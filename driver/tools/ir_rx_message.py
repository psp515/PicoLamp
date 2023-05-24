from enums.receiver_enum import ReceiveState


class IRReceiveMessage:
    """
    Class created for passing information from receiver classes to callbacks.
    Class assumes that ReceiveState.OK and ReceiveState.REPEAT are successes.
    """
    _state: ReceiveState
    _command: int
    _address: int

    def __init__(self, state: ReceiveState, command: int = None, address: int = None):
        self._state = state
        self._command = command
        self._address = address

    @property
    def state(self):
        """
        Informs if receive action was successfull.
        :return: ReceiveState enum element.
        """
        return self._state

    @property
    def command(self):
        """
        Informs of received command if state is ReceiveState.OK.
        :return: If action was successfull positive integer else -1.
        """
        if self._state is ReceiveState.OK or self._state is ReceiveState.REPEAT:
            return self._command

        return -1

    @property
    def address(self):
        """
        Informs of received address if state is ReceiveState.OK.
        :return: If action was successfull positive integer else -1.
        """
        if self._state is ReceiveState.OK or self._state is ReceiveState.REPEAT:
            return self._address

        return -1

    @property
    def is_succesfull(self):
        """
        Function created to convert ReceiverState to boolean.
        :return: True if read action was successfull and data is valid else False.
        """
        return True if self._state is ReceiveState.OK or self._state is ReceiveState.REPEAT else False
