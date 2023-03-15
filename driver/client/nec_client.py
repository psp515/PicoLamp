

class NecClient:
    def __init__(self, nec_ir: NECReceiver,
                 device_state: DeviceState,
                 logger: Logger):
        self.nec_ir = nec_ir
        self.device_state = device_state
        self.logger = logger
        self.topics = {}
    
    def callback(self, message: IRReceiveMessage):
        if not message.isSuccesfull():
            return

        function = self.topics[message.command]

        function(device_state, logger)

    def watch_topic(self, topic, callback):
        self.topics[topic] = callback
