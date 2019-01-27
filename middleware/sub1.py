import zmq
import json

class SubscriberDirectly:

    def __init__(self, config):
        self.config = config
        self.socket = None

    def register(self, topic):
        context = zmq.Context()
        socket_broker = context.socket(zmq.REQ)
        socket_broker.connet("tcp://%s" % self.config['broker'])
        socket_broker.send_json({'type': 'add_subscriber', 'ip': self.config['ip'], 'topic':topic})
        pub_ip = socket_broker.recv_string()
        assert pub_ip, 'no publisher for this topic: '%topic
        context = zmq.Context()
        socket_pub = context.socket(zmq.SUB)
        socket_pub.connect("tcp://*" % pub_ip)

    def notify(self):
        msg_str = self.socket.recv_json()
        msg = json.loads(msg_str)
        print('receive a message: topic=%s, value=%s'%(msg['Topic'], msg['Value']))
        self.socket.send_string('success')

class SubscriberViaBroker:

    def __init__(self, config):
        self.config = config
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % config['port'])
        self.socket = socket

    def register(self, topic):
        context = zmq.Context()
        socket_broker = context.socket(zmq.REQ)
        socket_broker.connet("tcp://%s" % self.config['broker'])
        socket_broker.send_json({'type': 'add_subscriber', 'ip': self.config['ip'], 'topic':topic})

    def notify(self):
        msg_str = self.socket.recv_json()
        msg = json.loads(msg_str)
        print('receive a message: topic=%s, value=%s'%(msg['Topic'], msg['Value']))
        self.socket.send_string('success')