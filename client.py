import os
import sys
import socket

# Constatnt parameters
message_max_size = 1024

# Get the user input or catch the exit signal
def get_input(prompt):
	try:
		return input(prompt)
	except EOFError:
		print (os.linesep + "user quit.")
		sys.exit(0)

while True:
	# Create the client socket. For every request exits one conection
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((socket.gethostname(), 1234))
	client_socket.setblocking(False)

	# Get the user input
	message = get_input(">")

	# Send the message to the server
	if message:
		message = message.encode('utf-8')
		client_socket.send(message)

	# Wait for the response of the server
	while True:
		try:
			response = client_socket.recv(message_max_size)
			print(response.decode('utf-8').strip())
			break
		except:
			continue
