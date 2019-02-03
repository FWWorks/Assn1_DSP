from application.broker import Broker
from configobj import ConfigObj
import sys

if len(sys.argv) == 2:
    config_path = sys.argv[1]
else:
    config_path = 'config/broker.ini'

if len(sys.argv) == 3:
    item = sys.argv[3]
else:
    item = 'Broker1'

config = ConfigObj(config_path)
broker = Broker(config=config[item])

broker.start()
