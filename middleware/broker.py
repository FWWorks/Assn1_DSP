import zmq
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
            if t not in self.topics:
                self.topics[t] = {'pub': set(), 'sub': set()}
            self.topics[t]['pub'].add(pub)
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
            if t not in self.topics:
                self.topics[t] = {'pub': set(), 'sub': set()}
            self.topics[t]['sub'].add(sub)
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
        if sub in self.subs and not self.subs[sub]['topics']:
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

class BrokerBase:

    def __init__(self, config):
        self.config = config
        self.table = RegisterTable()
        self.req_handler = {
            'add_publisher': self._add_pub,
            'pub_unregister_topic': self._pub_unregister_topic,
            'pub_exit_system': self._pub_exit_system,
            'pub_heartbeat': self._pub_heartbeat,
            'add_subscriber': self._add_sub,
            'sub_unregister_topic': self._sub_unregister_topic,
            'sub_exit_system': self._sub_exit_system,
            'sub_heartbeat': self._sub_heartbeat,
        }
        self.socket = None

    def handle_req(self):
        req = self.socket.recv_json()
        if isinstance(req, str):
            req = json.loads(req)
        result = self.req_handler[req['type']](req)
        print('request=%s, response=%s'%(req, result))
        self.socket.send_json({'msg': result})

    def _add_pub(self, req):
        result = self.table.add_pub(pub=req['ip'], topics=req['topic'])
        return result

    def _add_sub(self, req):
        result = self.table.add_sub(sub=req['ip'], topics=req['topic'])
        return result

    def _pub_unregister_topic(self,req):
        result = self.table.remove_pub(pub=req['ip'], topics=req['topic'])
        return result

    def _pub_exit_system(self, req):
        topics = self.table.get_pub_info(req['ip']).get('topics', [])
        result = self.table.remove_pub(pub=req['ip'], topics=deepcopy(topics))
        return result

    def _sub_unregister_topic(self, req):
        result = self.table.remove_sub(sub=req['ip'], topics=req['topic'])
        return result

    def _sub_exit_system(self, req):
        topics = self.table.get_sub_info(req['ip']).get('topics', [])
        result = self.table.remove_sub(sub=req['ip'], topics=deepcopy(topics))
        return result

    def _pub_heartbeat(self, req):
        result = self.table.refresh_pub(pub=req['ip'])
        return result

    def _sub_heartbeat(self, req):
        print('xxxxxxxxxxxxxxxxxxxxxx')
        result = self.table.refresh_sub(sub=req['ip'])
        return result

class BrokerType1(BrokerBase):

    def __init__(self, config):
        super().__init__(config)
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % config['port'])
        self.socket = socket

    def _add_sub(self, req):
        super()._add_sub(req)
        pubs = self.table.get_pubs(req['topic'])
        if pubs:
            return pubs[0]
        else:
            return ''

class BrokerType2(BrokerBase):

    def __init__(self, config):
        super().__init__(config)
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % config['port'])
        self.socket = socket
        self.req_handler['publish_req'] = self._publish_req

    def _publish_req(self, req):
        subs = self.table.get_subs(req['topic'])
        res = []
        for ip in subs:
            context = zmq.Context()
            sub_socket = context.socket(zmq.REQ)
            sub_socket.setsockopt(zmq.LINGER, 0)
            sub_socket.RCVTIMEO = 1000
            sub_socket.connect(ip)
            sub_socket.send_json({"topic": req['topic'], "value": req['value']})
            try:
                result = sub_socket.recv_json()
                res.append(result)
            except zmq.error.Again:
                res.append('fail to sub=%s'%ip)
            finally:
                sub_socket.close()
        return 'msg sent to ip=%s, res=%s' % (subs, res)