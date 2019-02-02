from middleware.broker import BrokerType1, BrokerType2
import time

class Broker:

    def __init__(self, config):
        self.config = config

    def start(self):
        broker = BrokerType1(self.config)
        # broker = BrokerType2(self.config)
        while True:
            broker.handle_req()