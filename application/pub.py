from middleware.pub import *

class Publisher:
    def __init__(self, mode, ip_address=None, strength=0):
        self.ip_address = ip_address
        self.strength = strength
        if mode == 1:
            self.pub_mw = PublisherDirectly(self.ip_address)
        elif mode == 2:
            self.pub_mw = PublisherViaBroker()
        else:
            print ("mode error, please choose approach")


    def publish(self, topic, value):
        return 0

    def register(self, topic):
        self.pub_mw.register()
        return 0

    def unregister(self, topic):
        return 0

    def drop_system(self):
        return 0

    def get_ip_address(self):
        return self.ip_address

    def get_strength(self):
        return self.strength

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address
        return 0

    def set_strength(self, strength):
        self.strength = strength
        return 0


p = Publisher(1, "tcp://127.0.0.1:5000")
p.pub_mw.register()

