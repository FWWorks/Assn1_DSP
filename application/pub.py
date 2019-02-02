from middleware.pub import *
import threading,time,socket

class Publisher:
    def __init__(self, mode, ip_address=None, broker_address=None, strength=0):
        self.ip_address = ip_address
        self.strength = strength
        self.heartthread = threading.Thread(self.send_heart_beat)
        if mode == 1:
            self.pub_mw = PublisherDirectly(self.ip_address, broker_address)
        elif mode == 2:
            self.pub_mw = PublisherViaBroker(self.ip_address, broker_address)
        else:
            print("mode error, please choose approach")

    def publish(self, topic, value):
        self.pub_mw.publish(topic, value)
        return 0

    def register(self, topic):
        self.pub_mw.register(topic)
        if self.heartthread.is_alive() == False:
            self.heartthread.start()
        return 0

    '''
    publisher cancels a topic
    '''
    def unregister_topic(self, topic):
        self.pub_mw.unregister(topic)
        return 0

    '''
    publish wants to exit the system
    '''
    def drop_system(self):
        self.pub_mw.drop_system()
        self.heartthread.stop()
        return 0

    '''
    send heart beat
    '''
    def send_heart_beat(self):
        while True:
            time.sleep(5)
            self.pub_mw.socket_heartbeat.send_json((json.dumps({'type': 'pub_heartbeat', 'ip': self.ip_address, 'mess': "1"})))
        return 0


    def get_ip_address(self):
        return self.ip_address

    def get_strength(self):
        return self.strength

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address
        return 0

    def set_strength(self, strength):
        self.strength = strength
        return 0


import time
p = Publisher(2, "tcp://127.0.0.1:5000", "tcp://localhost:5555")
p.register("hello")
while 1:
    x = input('msg=')
    p.publish("hello", x)
    time.sleep(1)

