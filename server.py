import zmq
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5000")
while True:
    msg = raw_input('input data:')
    socket.send(msg)

