import time
import zmq
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
# socket.setsockopt(zmq.SUBSCRIBE,'')
while True:
    print (socket.recv_string())
