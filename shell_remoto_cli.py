import os
import sys
import socket

# Message header size and message size
HEADER_SIZE = 32

# Get the user input from prompt
def get_input(msg: str):
	try:
		return input(msg)
	except EOFError:
		print (os.linesep + "user quit.")
		sys.exit(0)

# Set the correct format of the message to be sended
def message_format(message: str, h_size: int):
	return ('{msg:<{sz}}'.format(msg = len(message), sz = h_size) + message)

# Make client requests and wait for server responses
def cli(ip: str, port: int):
	while True:
		# Creating the socket TCP
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		message = get_input(">")

		# Making the conection with the server
		client_socket.connect((ip, port))
		client_socket.setblocking(False)

		if message:
			message = message
			message = message_format(message, HEADER_SIZE)
			client_socket.send(message.encode('utf-8'))

		# Waiting for the response from server
		is_header = False
		full_message = ''
		message_size = 0
		while True:
			try:
				response = client_socket.recv(HEADER_SIZE)
			except:
				continue
			
			if is_header: 
				full_message += response.decode('utf-8')
				message_size -= HEADER_SIZE
			else:
				message_size = int(response.decode('utf-8').strip())
				is_header = True
				continue

			if message_size <= 0 and len(full_message) > 0:
				print(full_message)
				break

# User error output
def badUse(message: str):
	print(message)
	print("Expected use: shell_remoto_cli -i <dir-ip> -p <puerto_svr>")
	return 0

# User error output
def main():
	# Check correctness of the input
	if len(sys.argv) < 5:
		badUse("Not enough arguments")
		return 1
	
	firstFlag	= sys.argv[1]
	firstParam	= sys.argv[2]
	secondFlag	= sys.argv[3]
	secondParam	= sys.argv[4]

	# Run client
	if firstFlag == "-i" and secondFlag == "-p":
		cli(str(firstParam),int(secondParam))
	elif firstFlag == "-p" and secondFlag == "-i":
		cli(str(secondParam),int(firstParam))
	else:
		badUse("Incorrect syntax")

if __name__ == "__main__":
    main()
