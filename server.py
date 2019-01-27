import zmq
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5000")
while True:
    msg = input('input data:')
    socket.send_string(msg)

