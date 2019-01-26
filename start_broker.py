from application.broker import Broker

broker = Broker(config={'port': '5555'})

broker.start()
