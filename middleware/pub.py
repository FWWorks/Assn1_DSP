import zmq
import json

class PublisherDirectly:
    def __init__(self, ip_address, broker_address, strength=None):
        self.ip_address = ip_address
        self.strength = strength
        self.socket = None
        self.broker_address = broker_address
        self.socket_broker = None
        self.context = zmq.Context()

    def publish(self, topic, value):
        if self.socket == None:
            self.__socket_bind()
            # print ("haven't registered a publisher")
        else:
            # self.__socket_bind()
            self.socket.send_string(json.dumps({"Topic": topic, "Value": value}))
        return 0

    def register(self, topic):
        self.__socket_bind()
        self.__reg_broker(topic)
        return 0

    def __socket_bind(self):
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(self.ip_address)

    def __reg_broker(self, topic):
        context = zmq.Context()
        socket_broker = context.socket(zmq.REQ)
        socket_broker.connect(self.broker_address)
        socket_broker.send_json((json.dumps({'type': 'add_publisher', 'ip': self.ip_address, 'topic': topic})))


    def unregister(self):
        return 0

    def drop_system(self):
        return 0



class PublisherViaBroker:
    def __init__(self, ip_address, broker_address, strength=None):
        self.ip_address = ip_address
        self.strength = strength
        self.socket = None
        self.broker_address = broker_address
        self.socket_broker = None
        self.context = zmq.Context()

    def publish(self, topic, value):
        if self.socket == None:
            print ("haven't registered a publisher")
        else:
            self.__socket_bind()
            self.socket.send_string(json.dumps({"Topic": topic, "Value": value}))
        return 0

    def register(self, topic):
        self.__socket_bind()
        self.__reg_broker(topic)
        return 0

    def __socket_bind(self):
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(self.ip_address)

    def __reg_broker(self, topic):
        context = zmq.Context()
        socket_broker = context.socket(zmq.REQ)
        socket_broker.connect(self.broker_address)
        socket_broker.send_json((json.dumps({'type': 'add_publisher', 'ip': self.ip_address, 'topic': topic})))


    def unregister(self):
        return 0

    def drop_system(self):
        return 0

