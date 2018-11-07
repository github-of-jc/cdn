#!/usr/bin/env python2.7
#client: nc localhost 1236
#this script: ./proxy.py 1236 127.0.0.1 8081
#server: nc -l 8081
import sys
import socket
import thread
import select
import time
import re
import signal
import argparse

def connect_client_to_server(conn, addr, threadNum, s, port, LOG, ALPHA, FAKE_IP):
	print('=====================================beginning of thread=' + str(threadNum))

	try:
		ss = socket.socket()
		server_ip = FAKE_IP
		server_port = 8080
		print('connect proxy to server at (fake) server ip', server_ip, ' port ', server_port)
		ss.connect((server_ip, server_port))
		print('ss connect successful')
		print('while conn')
		cdata = 1
		while cdata>0:
			print("client data is: \n" + str(cdata))
			print('recv data')
			cdata = conn.recv(1024)
			print('received cdata: ' + cdata)
			if len(cdata)>0:
				print(ss)
				
				try:
					print("trying to send cdata to ss")
					ss.send(cdata)
					print('expecting things back from server')
					sdata = ss.recv(1024)
					if len(sdata) > 0:
						print("server data is:\n" +  sdata)
						print('trying to send client the serve data')
						conn.send(sdata)
						print('successful sending server data to client')
				except:
					print('uh oh cannot send cdata to server')
					try:
						print('try reestablish connection to server')
						ss = socket.socket()
						server_ip = FAKE_IP
						server_port = 8080
						print('connect proxy to server at server ip', server_ip, ' port ', server_port)
						ss.connect((server_ip, server_port))
						print('ss connect successful')
						print('while conn')
					except:
						print('cannot reestablish connection to server, break client connection')
						conn.close()
						break
			else:
				print('client data is empty, break')
				break
		print("closing client connection")
		conn.close()
		print('client connection closed')
		print('closing server connection')
		ss.close()
		print('server connection closed')
	except:
		print('uh oh cannot send client data to server')
		try:
			print('try reestablish connection to server')
			ss = socket.socket()
			server_ip = FAKE_IP
			server_port = 8080
			print('connect proxy to server at server ip', server_ip, ' port ', server_port)
			ss.connect((server_ip, server_port))
			print('ss connect successful')
			print('while conn')
		except:
			print('cannot reestablish connection to server, break')
			conn.close()
				
#./proxy <log> <alpha> <listen-port> <fake-ip> <web-server-ip>


# listen for connections from a browser on any IP address on 
# the port specified as a command line argument

# accept multiple concurrent connections from web browsers
# by starting a new thread or process 
# for each new request

# when proxy connects to a server
# proxy bind the socket to the fake IP address from command line

parser = argparse.ArgumentParser()
parser.add_argument('log') 
parser.add_argument('alpha') 
# the TCP port the proxy should listen on for accepting connection from browser
parser.add_argument('listen_port') 
# proxy bound to fake_ip for outbound connection to web servers
# fake_ip can only be on of the clients' IP addresses under the network topo specified
parser.add_argument('fake_ip')
# ip address of the web server that proxy request video chuncks from 
# one of the servers IP addresses under the network topolocy specified
parser.add_argument('server_ip')

args = parser.parse_args()
LOG, ALPHA, LISTEN_PORT, FAKE_IP, SERVER_IP = args.log, args.alpha, args.listen_port, args.fake_ip, args.server_ip
print('finished parsing')
print(LOG, ALPHA, LISTEN_PORT, FAKE_IP, SERVER_IP)
s = socket.socket()
port = int(LISTEN_PORT)
s.bind(('', port))
print("socket binded to %s" %(port))
print('created socket, now listen')
s.listen(5) 
threadNum = 1

while True:
	print('=====================================beginning of client loop for thread=' + str(threadNum))
	print('# print conn, addr')
	conn, addr = s.accept()
	print('Connected by', addr)
	# open up connection with server
	# server socket
	print('created client connection')
	thread.start_new_thread(connect_client_to_server, (conn, addr, threadNum, s, port, LOG, ALPHA, FAKE_IP,))
	threadNum = threadNum + 1

print('end of program')








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
# c. close connections to the client and server when either disconnects'