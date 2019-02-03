from application.sub import Subscriber
from configobj import ConfigObj
import sys
import time

if len(sys.argv) == 2:
    config_path = sys.argv[1]
else:
    config_path = 'config/subscriber.ini'

if len(sys.argv) == 3:
    item = sys.argv[3]
else:
    item = 'Sub3'

config = ConfigObj(config_path)[item]

p = Subscriber(ip_self=config['sub_addr'], ip_broker=config['broker_addr'], comm_type=int(config['mode']))
p.register("hello1")
while 1:
    # p.notify()
    p.receive()
    time.sleep(1)