
class Publisher:
    def __init__(self, ip_address = None, strength = 0):
        self.ip_address = ip_address
        self.strength = strength
        return 0

    def publish(self, topic, value):
        return 0

    def register(self, topic):
        return 0

    def unregister(self, topic):
        return 0

    def drop_system(self):
        return 0

    def get_ip_address(self):
        return self.ip_address

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address
        return 0

    def set_strength(self, strength):
        self.strength = strength
        return 0

