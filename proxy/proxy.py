#!/usr/bin/env python2.7
import sys
import socket
import thread
import select
import time
import re
import signal
import argparse

# cd ~/project1-starter/proxy
# ./proxy <listen-port> <fake-ip> <server-ip>

parser = argparse.ArgumentParser()
parser.add_argument('listen_port') 
parser.add_argument('fake_ip')
parser.add_argument('server_ip')

args = parser.parse_args()
LISTEN_PORT, FAKE_IP, SERVER_IP = args.listen_port, args.fake_ip, args.server_ip
print('finished parsing')
print(LISTEN_PORT, FAKE_IP, SERVER_IP)
s = socket.socket()
port = int(LISTEN_PORT)
s.bind(('', port))
print("socket binded to %s" %(port))
print('created socket, now listen')
s.listen(5) 

print('print conn, addr')
conn, addr = s.accept()
print('Connected by', addr)
while True:

	#open up connection with server
	#server socket
	print('created socket')
	ss = socket.socket()
	server_ip = FAKE_IP
	server_port = 8081
	print('connect proxy to server at server ip', server_ip, ' port ', server_port)
	ss.connect((server_ip, server_port))
	print('ss connect successful')
	print('while conn')

	while True:
		print('recv data')
		data = conn.recv(1024)
		print(data)
		ss.send(data)
		print('if not data')
		if not data:
			print('conn.close')
			conn.close()
			ss.close()
			print('conn.closed, now break')
			break



# open up another connection with a server
# once both connections are established,
#  the proxy should forward messages between the client and server

# establish connection with a client
# a. listen for connections from a client on *any* IP accress on the port
#     specified on the command line argument
#    accept multiple connections from clients sequentially
# b. establish a connection with a server
#    (once established a connection to the client)
#    get server IP provided from command line argument
#    use 8080 for port number
# c. close connections to the client and server when either disconnects