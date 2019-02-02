import zmq
import json


class SubDirect:

    def __init__(self, ip_self, ip_broker):
        self.ip = ip_self
        self.ip_b = ip_broker
        self.context = zmq.Context()
        self.socket_sub = self.context.socket(zmq.REQ)
        self.socket_sub.connect(ip_broker)

    def register(self, topic):
        self.socket_sub.send_json(json.dumps({"type": "add_subscriber", "ip": self.ip, "topic": topic}))

    def receive(self):
        return self.socket_sub.recv_string()

    def unregister(self, topic):
        self.socket_sub.send_json(json.dumps({"type": "remove_subscriber", "ip": self.ip, "topic": topic}))

    def exit(self):
        self.socket_sub.send_json(json.dumps({"type": "exit_subscriber", "ip": self.ip, "topic": "all"}))


class SubBroker(SubDirect):

    def __init__(self, ip_self, ip_broker):
        print(ip_self, ip_broker, 'xxxxxxxxxxxxxxxxxxxxxxxxxx')
        super().__init__(ip_self, ip_broker)
        self.ip = ip_self
        self.ip_b = ip_broker
        self.context = None
        self.socket_sub = None
        self.socket_ntf = None

    def register(self, topic):
        self.context = zmq.Context()
        self.socket_sub = self.context.socket(zmq.REQ)
        self.socket_sub.connect(self.ip_b)

        context = zmq.Context()
        self.socket_ntf = context.socket(zmq.REP)
        self.socket_ntf.bind(self.ip)
        self.socket_sub.send_json({"type": "add_subscriber", "ip": self.ip, "topic": topic})

    def notify(self):

        msg = self.socket_ntf.recv_json()
        print("receive a message: topic = %s, value = %s" % (msg["topic"], msg["value"]))
        self.socket_ntf.send_string("success")
