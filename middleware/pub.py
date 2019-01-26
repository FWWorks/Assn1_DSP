import zmq
import json

class PublisherDirectly:
    def __init__(self, ip_address, broker_address, strength=None):
        self.ip_address = ip_address
        self.strength = strength
        self.socket = ""
        self.broker_address = broker_address
        self.socket_broker = None


    def publish(self, topic, value):



        return 0

    def register(self, topic):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(self.ip_address)
        socket_broker = context.socket(zmq.REQ)
        socket_broker.connect(self.broker_address)
        socket_broker.send_json((json.dumps({'type': 'add_publisher', 'ip':self.ip_address, 'topic': topic})))
        return 0

    def unregister(self):
        return 0

    def drop_system(self):
        return 0



class PublisherViaBroker:
    pass
