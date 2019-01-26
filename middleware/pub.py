import zmq
class PublisherDirectly:
    def __init__(self, ip_address, strength = None):
        self.ip_address = ip_address
        self.strength = strength

    def publish(self, ip_address, topic, value):
        return 0

    def register(self):
        return 0

    def unregister(self):
        return 0

    def drop_system(self):
        return 0



class PublisherViaBroker:
    pass
