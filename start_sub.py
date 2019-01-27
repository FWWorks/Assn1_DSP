from application.sub1 import Subscriber

subscriber = Subscriber({'broker': 'localhost:5555', 'ip':'localhost', 'port': 5000})

subscriber.register('weather')
subscriber.receive()