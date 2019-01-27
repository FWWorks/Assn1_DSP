from middleware.sub1 import SubscriberDirectly, SubscriberViaBroker


class Subscriber:

    def __init__(self, config):
        self.config = config
        self.sub_mid = SubscriberDirectly(config)

    def register(self, topic):
        self.sub_mid.register(topic)

    def receive(self):
        while 1:
            self.sub_mid.notify()


