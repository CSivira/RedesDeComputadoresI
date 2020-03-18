import os
import sys
import socket

HEADER_SIZE = 16

def get_input(msg: str):
	try:
		return input(msg)
	except EOFError:
		print (os.linesep + "user quit.")
		sys.exit(0)

def message_format(message: str, h_size: int):
	return (f'{len(message):<{HEADER_SIZE}}' + message)

def cli(ip: str, port: int):
	while True:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((ip, port))
		client_socket.setblocking(False)

		message = get_input(">")

		if message:
			message = message
			message = message_format(message, HEADER_SIZE)
			client_socket.send(message.encode('utf-8'))

		is_header = False
		full_message = ''
		message_size = 0
		while True:
			try:
				response = client_socket.recv(HEADER_SIZE)
			except:
				continue
			
			if is_header: 
				full_message += response.decode('utf-8').strip()	
				message_size -= HEADER_SIZE
			else:
				message_size = int(response.decode('utf-8').strip(' '))
				is_header = True
				continue

			if message_size <= 0 and len(full_message) > 0:
				print(full_message)
				break

def badUse(message: str):
	print(message)
	print("Expected use: shell_remoto_cli -i <dir-ip> -p <puerto_svr>")
	return 0

def main():
	if len(sys.argv) < 5:
		badUse("Not enough arguments")
		return 1
	
	firstFlag	= sys.argv[1]
	firstParam	= sys.argv[2]
	secondFlag	= sys.argv[3]
	secondParam	= sys.argv[4]

	if firstFlag == "-i" and secondFlag == "-p":
		cli(str(firstParam),int(secondParam))
	elif firstFlag == "-p" and secondFlag == "-i":
		cli(str(secondParam),int(firstParam))
	else:
		badUse("Incorrect syntax")

if __name__ == "__main__":
    main()
