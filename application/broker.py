from middleware.broker import BrokerType1, BrokerType2

class Broker:

    def __init__(self, config):
        self.config = config

    def start(self):
        if int(self.config['mode']) == 1:
            broker = BrokerType1(self.config)
        else:
            broker = BrokerType2(self.config)
        while True:
            broker.handle_req()