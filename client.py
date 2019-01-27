import time
import zmq
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
# socket.setsockopt(zmq.SUBSCRIBE,'')
socket.connect("tcp://127.0.0.1:5000")
socket.setsockopt_string(zmq.SUBSCRIBE,'')
while True:
    print (socket.recv_string())
