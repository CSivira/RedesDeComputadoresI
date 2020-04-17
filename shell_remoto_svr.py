###############################################################################
#   Authors:                                                                  #
#       - Carlos Alejandro Sivira Muñoz   ---   15-11377     ###############  #
#       - José Ramón Barrera Melchor   ---   15-10123        ##           ##  #
#                                                                ###  ###     #
#   File Name: shell_remoto_svr.py                              ##      ##    #
#   Description: Client Socket Implementation with Python        ###  ###     #
#   Params:                                                  ##           ##  #
#       <port_svr>: Local address number                     ###############  #
#                                                                             #
###############################################################################

import os
import sys
import socket
from signal import signal, SIGINT

# Server locar IP
IP = "127.0.0.1"
# Message header size and message size
HEADER_SIZE = 32
# Maximun number of supported requests
MAX_NUMBER_REQUESTS = 8

# Exit secuence
def handler(signal_received, frame):
    # Handle any cleanup here
    print('\nSIGINT or CTRL-C detected. Shutting down the server')
    exit(0)

# Get output from external file
def get_output(file_name: str):
	try:
		file = open(file_name, 'r')
		content = str(file.read())
		file.close()
		os.system("rm " + file_name)
		return content.encode('utf-8')
	except:
		response = "The Shell couldn't execute the command properly"
		return response.encode('utf-8')

# Set the correct format of the message to be sended
def message_format(message: str, h_size: int):
	return ('{msg:<{sz}}'.format(msg = len(message), sz = h_size) + message)

# Listen messages from clients and give responses
def svr(port: int):
	# Creating the server socket
	server_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((IP, port))

	# Listen for clients requests
	server_socket.listen(MAX_NUMBER_REQUESTS)

	print('Running. Press CTRL-C to exit.')
	print('Waiting for clients...')

	while True:
		client_socket, address = server_socket.accept()
		print(f"Connection from {address} has been established.")

		# Waiting for the response from server
		is_header = False
		command = ''
		message_size = 0
		while True:
			try:
				response = client_socket.recv(HEADER_SIZE)
			except:
				continue
         
			if is_header:
				command += response.decode('utf-8')
				message_size -= HEADER_SIZE
			else:
				message_size = int(response.decode('utf-8').strip())
				is_header = True
				continue
        
			if message_size <= 0 and len(command) > 0:
				break

		command = command + f" > .output_{address[1]} 2>&1"
		os.system(command)

		response = get_output(f'.output_{address[1]}').decode('utf-8')
		response = message_format(response, HEADER_SIZE)

		client_socket.send(response.encode('utf-8'))
		client_socket.close()

# User error output
def badUse(message: str):
	print(message)
	print("Expected use: shell_remoto_svr -p <puerto_svr>")
	return 0

# Main function of the program
def main():
	# Check correctness of the input
	if len(sys.argv) < 3:
		badUse("Not enough arguments")
		return 1
	
	firstFlag	= sys.argv[1]
	firstParam	= sys.argv[2]

	# Run the server
	if firstFlag == "-p":
		svr(int(firstParam))
	else:
		badUse("Incorrect syntax")

if __name__ == "__main__":
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    main()
