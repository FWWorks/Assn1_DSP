import zmq
from collections import defaultdict
import json
from datetime import datetime
from copy import deepcopy

class RegisterTable:

    def __init__(self):
        self.pubs = {}
        self.subs = {}
        self.topics = {}

    def add_pub(self, pub, topics):
        if isinstance(topics, str):
            topics = [topics]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if pub in self.pubs:
            self.pubs[pub]['since'] = now
            self.pubs[pub]['topics'].update(topics)
        else:
            self.pubs[pub] = {'since': now, 'topics': set(topics)}
        for t in topics:
            if t in self.topics:
                self.topics[t]['pub'].add(pub)
            else:
                self.topics[t] = {'pub': set(), 'sub':set()}
        return ''

    def add_sub(self, sub, topics):
        if isinstance(topics, str):
            topics = [topics]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if sub in self.subs:
            self.subs[sub]['since'] = now
            self.subs[sub]['topics'].update(topics)
        else:
            self.subs[sub] = {'since': now, 'topics': set(topics)}
        for t in topics:
            if t in self.topics:
                self.topics[t]['sub'].add(sub)
            else:
                self.topics[t] = {'pub': set(), 'sub':set()}
        return ''

    def remove_pub(self, pub, topics):
        if isinstance(topics, str):
            topics = [topics]
        for t in topics:
            print(t)
            try:
                self.pubs[pub]['topics'].remove(t)
                self.topics[t]['pub'].remove(pub)
            except KeyError:
                pass
        if pub in self.pubs and not self.pubs[pub]['topics']:
            self.pubs.pop(pub)
        return ''

    def remove_sub(self, sub, topics):
        if isinstance(topics, str):
            topics = [topics]
        for t in topics:
            try:
                self.subs[sub]['topics'].remove(t)
                self.topics[t]['sub'].remove(sub)
            except KeyError:
                pass
        if sub in self.subs and not self.pubs[sub]['topics']:
            self.subs.pop(sub)
        return ''

    def refresh_sub(self, sub):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if sub in self.subs:
            self.subs[sub]['since'] = now
        return now

    def refresh_pub(self, pub):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if pub in self.pubs:
            self.pubs[pub]['since'] = now
        return now

    def get_pubs(self, topic):
        if topic not in self.topics:
            return []
        return list(self.topics[topic]['pub'])

    def get_subs(self, topic):
        if topic not in self.topics:
            return []
        return list(self.topics[topic]['sub'])

    def get_pub_info(self, pub):
        return self.pubs.get(pub, {})

    def get_sub_info(self, pub):
        return self.pubs.get(pub, {})

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
            if req['ip'] not in self.table[req['topic']]:
                self.table[req['topic']].append(req['ip'])
                self.socket.send_string('success')
            else:
                self.socket.send_string('already existed. ip=%s, topic=%s'%(req['ip'], req['topic']))
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
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % config['port'])
        self.socket = socket
        self.table = RegisterTable()

    def handle_req(self):
        req = self.socket.recv_json()
        print(req)
        if isinstance(req, str):
            req = json.loads(req)

        if req['type'] == 'add_publisher':
            print('add a publisher. ip=%s, topic=%s' % (req['ip'], req['topic']))
            result = self.table.add_pub(pub=req['ip'], topics=req['topic'])
            self.socket.send_json({'msg': result})

        elif req['type'] == 'add_subscriber':
            print('add a subscriber. ip=%s, topic=%s'%(req['ip'], req['topic']))
            result = self.table.add_sub(sub=req['ip'], topics=req['topic'])
            self.socket.send_json({'msg': result})

        elif req['type'] == 'pub_unregister_topic':
            print('unregister a topic from pub. ip=%s, topic=%s' % (req['ip'], req['topic']))
            result = self.table.remove_pub(pub=req['ip'], topics=req['topic'])
            self.socket.send_json({'msg': result})

        elif req['type'] == 'pub_exit_system':
            print('pub exit. ip=%s' % (req['ip']))
            topics = self.table.get_pub_info(req['ip']).get('topics', [])
            result = self.table.remove_pub(pub=req['ip'], topics=deepcopy(topics))
            self.socket.send_json({'msg': result})

        elif req['type'] == 'sub_unregister_topic':
            print('unregister a topic from sub. ip=%s, topic=%s' % (req['ip'], req['topic']))
            result = self.table.remove_sub(sub=req['ip'], topics=req['topic'])
            self.socket.send_json({'msg': result})

        elif req['type'] == 'sub_exit_system':
            print('sub exit. ip=%s' % (req['ip']))
            topics = self.table.get_sub_info(req['ip']).get('topics', [])
            result = self.table.remove_sub(sub=req['ip'], topics=deepcopy(topics))
            self.socket.send_json({'msg': result})

        elif req['type'] == 'pub_heartbeat':
            result = self.table.refresh_pub(pub=req['ip'])
            print('heartbeat from pub.ip=%s. msg=%s' % (req['ip'], result))
            self.socket.send_json({'msg': result})

        elif req['type'] == 'sub_heartbeat':
            result = self.table.refresh_sub(sub=req['ip'])
            print('heartbeat from sub.ip=%s. msg=%s' % (req['ip'], result))
            self.socket.send_json({'msg': result})

        elif req['type'] == 'publish_req':
            subs = self.table.get_subs(req['topic'])
            for ip in subs:
                context = zmq.Context()
                sub_socket = context.socket(zmq.REQ)
                sub_socket.connect(ip)
                sub_socket.send_json({"topic": req['topic'], "value": req['value']})
                result = sub_socket.recv_string()
                print('msg sent to ip=%s, result=%s' % (ip, result))
            self.socket.send_json({})