import zmq
from collections import defaultdict
import json

class BrokerType1:

    def __init__(self, config):
        self.config = config
        self.table = defaultdict(list)
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s"%config['port'])
        self.socket = socket

    def handle_req(self):
        req_str = self.socket.recv_json()
        req = json.loads(req_str)

        if req['type'] == 'add_publisher':
            print('add a publisher. ip=%s, topic=%s'%(req['ip'], req['topic']))
            self.table[req['topic']].append(req['ip'])
            self.socket.send_string('success')

        elif req['type'] == 'add_subscriber':
            print('add a subscriber')
            if req['topic'] in self.table:
                pub_ip = self.table[req['topic']][0]
                print('publisher ip = %s'%pub_ip)
                self.socket.send_string(pub_ip)
            else:
                self.socket.send_string('')

class BrokerType2:pass
