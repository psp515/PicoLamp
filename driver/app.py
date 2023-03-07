

class App:
    device: Device
    logger: Logger
    client: HivemqMQTTClient
    wlan: WLAN
    topics: []

    def __init__(self,
                 device: Device,
                 logger: Logger,
                 client: HivemqMQTTClient,
                 wlan: WLAN,
                 topics: []):
        self.wlan = wlan
        self.client = client
        self.logger = logger
        self.device = device
        self.topics = topics

    def start(self):

        #TODO start second thread

        while True:
            if self.wlan.isconnected():
                for topic in self.topics:
                    self.client.subscribe(topic)

                if self.device.un_pushed_changes:
                    # TODO
                    # publish data with mqtt
                    # on topics but with '_device' signature ??
                    pass
            else:
                self.logger.log("Device disconnected from internet.", LoggerEnum.WARNING)
                sleep(1)
