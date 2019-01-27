from middleware.pub import *

class Publisher:
    def __init__(self, mode, ip_address=None, broker_address=None, strength=0):
        self.ip_address = ip_address
        self.strength = strength
        if mode == 1:
            self.pub_mw = PublisherDirectly(self.ip_address, broker_address)
        elif mode == 2:
            self.pub_mw = PublisherViaBroker(self.ip_address, broker_address)
        else:
            print ("mode error, please choose approach")


    def publish(self, topic, value):
        self.pub_mw.publish(topic, value)
        return 0

    def register(self, topic):
        self.pub_mw.register(topic)
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


import time
p = Publisher(2, "tcp://127.0.0.1:5000", "tcp://localhost:5555")
p.register("hello")
while 1:
    p.publish("hello", "555")
    time.sleep(1)

