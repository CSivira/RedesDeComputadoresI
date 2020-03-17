import os
import socket

def get_input(msg):
    try:
        return input(msg)
    except EOFError:
        print (os.linesep + "user quit.")
        sys.exit(0)

def server_solicitude(server, r):
	    server.send(bytes(r,"utf-8"))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))
	
while True:
	req = get_input(">")
	server_solicitude(s, req)