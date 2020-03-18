import socket
import sys
import os

IP = "127.0.0.1"

# Get output from external file
def get_output(file_name: str):
	file = open(file_name, 'r')
	content = str(file.read())
	file.close()
	os.system("rm output*")
	return content.encode('utf-8')

def svr(port: int):
	# Constant parameters
	message_max_size = 1024

	# Creating the server socket
	server_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((IP, port))

	# Listen for clients requests
	server_socket.listen(5)

	print('Waiting for clients...')

	while True:
		client_socket, address = server_socket.accept()
		message = client_socket.recv(message_max_size)
		print(f"Connection from {address} has been established.")

		command = message.decode('utf-8').strip()
		command = command + f" > output_{address[1]}"
		
		os.system(command)

		client_socket.send(get_output(f"output_{address[1]}"))
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
    main()