import socket

HEADERSIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
	clientsocket, address = s.accept()
	msg = clientsocket.recv(HEADERSIZE)
	print(f"Connection from {address} has been established.")
	print(msg)
	clientsocket.send(bytes("response","utf-8"))
	clientsocket.close()