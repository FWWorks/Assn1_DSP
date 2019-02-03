import time
from middleware.sub import *

sub_direct = 1
sub_broker = 2


class Subscriber:

    def __init__(self, ip_self, ip_broker, comm_type):
        self.ip = ip_self
        self.ip_b = ip_broker
        if comm_type == sub_direct:
            self.sub_mid = SubDirect(self.ip, self.ip_b)
        elif comm_type == sub_broker:
            self.sub_mid = SubBroker(self.ip, self.ip_b)
        else:
            print("Error in communication type: Only 1 and 2 are accepted.")
            exit(1)
        self.comm_type = comm_type

    def register(self, topic):
        self.sub_mid.register(topic)

    def receive(self):
        if self.comm_type == sub_direct:
            self.sub_mid.receive()
        if self.comm_type == sub_broker:
            self.sub_mid.notify()

    def unregister(self, topic):
        self.sub_mid.unregister(topic)

    def exit(self):
        self.sub_mid.exit()



