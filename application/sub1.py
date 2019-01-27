from middleware.sub1 import SubscriberDirectly, SubscriberViaBroker


class Subscriber:

    def __init__(self, config):
        self.config = config
        self.sub_mid = SubscriberDirectly(config)
    pass

    def start(self):
        self.sub_mid.register(self.config['topic'])
        while 1:
            self.sub_mid.notify()


