import zmq
import json


class Subscriber1:

    def __init__(self, ip_self, ip_broker):
        self.ip = ip_self
        self.ip_b = ip_broker
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://" + ip_broker + ":5555")
    pass

    def register(self, topic):
        self.socket.send_json(json.dump({"type": "add_subscriber", "ip": self.ip, "topic": topic}))
    pass

    def receive(self):
        return self.socket.recv_string()
    pass

    def unregister(self, topic):
        self.socket.send_json(json.dump({"type": "remove_subscriber", "ip": self.ip, "topic": topic}))
    pass

    def exit(self):
        self.socket.send_json(json.dump({"type": "exit_subscriber", "ip": self.ip, "topic": "all"}))
    pass


pass
