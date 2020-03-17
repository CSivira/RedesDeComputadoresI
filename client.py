import os
import sys
import socket

def get_input(msg):
	try:
		return input(msg)
	except EOFError:
		print (os.linesep + "user quit.")
		sys.exit(0)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 1234))
client_socket.setblocking(False)

while True:
	message = get_input(">")

	if message:
		message = message.encode('utf-8')
		client_socket.send(message)

	while True:
		try:
			response = client_socket.recv(1024)
			print(response.decode('utf-8').strip())
			break
		except:
			continue
