import zmq
from collections import defaultdict
import json


class BrokerType1:

    def __init__(self, config):
        self.config = config
        self.table = defaultdict(list)
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % config['port'])
        self.socket = socket

    def handle_req(self):
        req = self.socket.recv_json()

        if isinstance(req, str):
            req = json.loads(req)

        if req['type'] == 'add_publisher':
            print('add a publisher. ip=%s, topic=%s' % (req['ip'], req['topic']))
            self.table[req['topic']].append(req['ip'])
            self.socket.send_string('success')

        elif req['type'] == 'add_subscriber':
            print('add a subscriber')
            if req['topic'] in self.table:
                pub_ip = self.table[req['topic']][0]
                print('publisher ip = %s' % pub_ip)
                self.socket.send_string(pub_ip)
            else:
                self.socket.send_string('')


class BrokerType2:

    def __init__(self, config):
        self.config = config
        self.table = {}
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % config['port'])
        self.socket = socket

    def handle_req(self):
        req_str = self.socket.recv_json()
        req = json.loads(req_str)

        if req['type'] == 'add_publisher':
            print('add a publisher. ip=%s, topic=%s' % (req['ip'], req['topic']))

            if req['topic'] in self.table:
                self.table[req['topic']]['pub'].append(req['ip'])
            else:
                self.table[req['topic']] = {'pub': [req['ip']], 'sub': []}
            self.socket.send_string('success')

        elif req['type'] == 'add_subscriber':
            print('add a subscriber. ip=%s, topic=%s'%(req['ip'], req['topic']))
            if req['topic'] in self.table:
                self.table[req['topic']]['sub'].append(req['ip'])
            else:
                self.table[req['topic']] = {'pub': [], 'sub': [req['ip']]}

        elif req['type'] == 'publish':
            assert req['topic'] in self.table
            subs = self.table[req['topic']]['sub']
            for ip in subs:
                context = zmq.Context()
                sub_socket = context.socket(zmq.REQ)
                sub_socket.connect("tcp://%s" % ip)
                sub_socket.send_json({"Topic": req['topic'], "Value": req['value']})
                result = sub_socket.recv_string()
                print('msg sent to ip=%s, result=%s' % (ip, result))
