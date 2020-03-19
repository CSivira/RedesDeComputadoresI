import os
import sys
import socket
from signal import signal, SIGINT

IP = "127.0.0.1"
HEADER_SIZE = 16
MAX_NUMBER_SOLICITUDES = 8

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
		os.system("rm .output*")
		return content.encode('utf-8')
	except:
		response = "The Shell couldn't execute the command properly"
		return response.encode('utf-8')

def message_format(message: str, h_size: int):
	return (f'{len(message):<{HEADER_SIZE}}' + message)

def svr(port: int):
	# Creating the server socket
	server_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((IP, port))

	# Listen for clients requests
	server_socket.listen(MAX_NUMBER_SOLICITUDES)

	print('Running. Press CTRL-C to exit.')
	print('Waiting for clients...')

	while True:
		client_socket, address = server_socket.accept()
		print(f"Connection from {address} has been established.")

		is_header = False
		command = ''
		message_size = 0
		while True:
			try:
				response = client_socket.recv(HEADER_SIZE)
			except:
				continue
         
			if is_header:
				command += response.decode('utf-8').strip()
				message_size -= HEADER_SIZE
			else:
				print(int(response.decode('utf-8').strip(' ')))
				message_size = int(response)
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

def badUse(message: str):
	print(message)
	print("Expected use: shell_remoto_svr -p <puerto_svr>")
	return 0

def main():
	if len(sys.argv) < 3:
		badUse("Not enough arguments")
		return 1
	
	firstFlag	= sys.argv[1]
	firstParam	= sys.argv[2]

	if firstFlag == "-p":
		svr(int(firstParam))
	else:
		badUse("Incorrect syntax")

if __name__ == "__main__":
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    main()
