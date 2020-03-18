import os
import sys
import socket

def get_input(msg):
	try:
		return input(msg)
	except EOFError:
		print (os.linesep + "user quit.")
		sys.exit(0)

def cli(ip, port):
	while True:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((ip, port))
		client_socket.setblocking(False)

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

def badUse(message):
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

	print("firstFlag = "+firstFlag)
	print("firstParam = "+firstParam)
	print("secondFlag = "+secondFlag)
	print("secondParam = "+secondParam)

	if firstFlag == "-i" and secondFlag == "-p":
		cli(str(firstParam),int(secondParam))
	elif firstFlag == "-p" and secondFlag == "-i":
		cli(int(secondParam),str(firstParam))
	else:
		badUse("Incorrect syntax")

if __name__ == "__main__":
    main()