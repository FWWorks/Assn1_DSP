import zmq
import time
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")
while True:
    # msg = input('input data:')
    print('123')
    socket.send_string('123')
    time.sleep(1)


