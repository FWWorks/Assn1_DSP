from middleware.sub import *


class Subscriber:

    def __init__(self, ip_self, ip_broker):
        self.ip = ip_self
        self.ip_b = ip_broker
        self.sub_mid = Subscriber1(self.ip, self.ip_b)
    pass

    def register(self, topic):
        self.sub_mid.register(topic)
    pass

    def receive(self):
        print(self.sub_mid.sub_receive())
        self.sub_mid.receive()
    pass

    def unregister(self, topic):
        self.sub_mid.unregister(topic)
    pass

    def exit(self):
        self.sub_mid.exit()
    pass


pass
