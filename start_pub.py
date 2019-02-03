from application.pub import Publisher
from configobj import ConfigObj
import sys
import time

if len(sys.argv) == 2:
    config_path = sys.argv[1]
else:
    config_path = 'config/publisher.ini'

if len(sys.argv) == 3:
    item = sys.argv[3]
else:
    item = 'Pub3'

config = ConfigObj(config_path)[item]

p = Publisher(mode=int(config['mode']), ip_address=config['pub_addr'],
              broker_address=config['broker_addr'], strength=config['strength'])
topic = 'hello1'
# p.register("hello")
p.register(topic)
# for i in range(300):
print('pub ip=%s. topic=%s'%(p.ip_address, topic))
while 1:
# for i in range(5):
    # x = input('ty')
    p.publish(topic, '555')
    time.sleep(1)

p.drop_system()