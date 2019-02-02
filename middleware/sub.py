import zmq
import json


class SubDirect:

    def __init__(self, ip_self, ip_broker):
        self.ip = ip_self
        self.ip_b = ip_broker
        self.context_sub = None
        self.context_rcv = None
        self.socket_sub = None
        self.socket_rcv = None

    def register(self, topic):
        self.context_sub = zmq.Context()
        self.socket_sub = self.context_sub.socket(zmq.REQ)
        self.socket_sub.connect(self.ip_b)

        self.socket_sub.send_json(json.dumps({"type": "add_subscriber", "ip": self.ip, "topic": topic}))

        self.context_rcv = zmq.Context()
        self.socket_rcv = self.context_rcv.socket(zmq.SUB)
        self.socket_rcv.setsockopt(zmq.SUBSCRIBE, b"hello")
        self.socket_rcv.connect(self.ip)

    def receive(self):
        msg = self.socket_rcv.recv_json()
        print("receive a message: topic = %s, value = %s" % (msg["topic"], msg["value"]))

    def unregister(self, topic):
        self.socket_sub.send_json(json.dumps({"type": "remove_subscriber", "ip": self.ip, "topic": topic}))

    def exit(self):
        self.socket_sub.send_json(json.dumps({"type": "exit_subscriber", "ip": self.ip, "topic": "all"}))


class SubBroker:

    def __init__(self, ip_self, ip_broker):
        # print(ip_self, ip_broker, 'XXX')
        self.ip = ip_self
        self.ip_b = ip_broker
        self.context_sub = None
        self.context_ntf = None
        self.socket_sub = None
        self.socket_ntf = None

    def register(self, topic):
        self.context_sub = zmq.Context()
        self.socket_sub = self.context_sub.socket(zmq.REQ)
        self.socket_sub.connect(self.ip_b)
        self.socket_sub.send_json({"type": "add_subscriber", "ip": self.ip, "topic": topic})

        self.context_ntf = zmq.Context()
        self.socket_ntf = self.context_ntf.socket(zmq.REP)
        self.socket_ntf.connect(self.ip)

    def notify(self):
        msg = self.socket_ntf.recv_json()
        print("receive a message: topic = %s, value = %s" % (msg["topic"], msg["value"]))
        self.socket_ntf.send_string("success")

    def unregister(self, topic):
        self.socket_sub.send_json(json.dumps({"type": "remove_subscriber", "ip": self.ip, "topic": topic}))

    def exit(self):
        self.socket_sub.send_json(json.dumps({"type": "exit_subscriber", "ip": self.ip, "topic": "all"}))