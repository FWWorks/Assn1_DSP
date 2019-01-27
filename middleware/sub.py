import zmq
import json


class Subscriber1:

    def __init__(self, ip_self, ip_broker):
        self.ip = ip_self
        self.ip_b = ip_broker
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
    pass

    def register(self, topic):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(self.ip_b)
        socket.send_json(json.dumps({"type": "add_subscriber", "ip": self.ip, "topic": topic}))
        res = socket.recv_string()
        print(res)
        self.socket.connect(res)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    pass

    def receive(self):
        print(self.socket.recv_string())
    pass

    def unregister(self, topic):
        self.socket.send_json(json.dumps({"type": "remove_subscriber", "ip": self.ip, "topic": topic}))
    pass

    def exit(self):
        self.socket.send_json(json.dump({"type": "exit_subscriber", "ip": self.ip, "topic": "all"}))
    pass


pass
