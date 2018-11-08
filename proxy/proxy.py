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

def recv_data(threadNum, conn, ss, fake_ip, server_port):
	cdata = ''
	print(str(threadNum) + 'entering while loop receiving data')

	print(str(threadNum) + 'cdata:' + str(cdata))
	print(str(threadNum) + 'recv cdata')
	packet = None
	packet = conn.recv(10000)
	print(str(threadNum) + 'packet is: \n' + packet)
	cdata = cdata + packet
	print(str(threadNum) + 'received cdata: ============================' + cdata)
	return cdata

def send_to_server(cdata, threadNum, conn, ss, fake_ip, server_port):
	if len(cdata)>0:
		print('len(cdata>0)')
		print(ss)
		sdata = ''
		
		try:
			print(str(threadNum) + "trying to send cdata to ss")
			ss.send(cdata)
			print(str(threadNum) + 'cdata sent to server')
			print(str(threadNum) + 'expecting things back from server')
			
			
			while 1:
				print(str(threadNum) + 'recv sdata')
				packet = ss.recv(10000)
				if packet:
					print(str(threadNum) + 'server packet is: \n' + packet)
					sdata = sdata + packet
				else:
					break
			if len(sdata) > 0:
				print(str(threadNum) + "server data is:===============================\n" +  sdata)
				print(str(threadNum) + 'trying to send client the server data')
				conn.send(sdata)
				print(str(threadNum) + 'successful sending server data to client')

		except:
			print(str(threadNum) + 'uh oh cannot send cdata to server')
			try:
				print(str(threadNum) + 'try reestablish connection to server')
				ss = socket.socket()
				server_port = 8080
				print(str(threadNum) + 'connect proxy to server at server ip', fake_ip, ' port ', server_port)
				ss.connect((fake_ip, server_port))
				print(str(threadNum) + 'ss connect successful, not sending or receiving tho')
			except:
				print(str(threadNum) + 'cannot reestablish connection to server, break client connection')
				conn.close()
				
	else:
		print(str(threadNum) + 'client data is empty, break')

def connect_client_to_server(conn, addr, threadNum, s, port, LOG, ALPHA, FAKE_IP):
	print('=====================================beginning of thread=' + str(threadNum))
	
	try:
		ss = socket.socket()
		fake_ip = FAKE_IP
		server_port = 8080
		print(str(threadNum) + 'bind server socket to fake IP address before connecting')
		ss.bind((fake_ip, server_port))
		print(str(threadNum) + 'bind successful')
		print(str(threadNum) + 'connect proxy to server at (fake) server ip', fake_ip, ' port ', server_port)
		ss.connect((fake_ip, server_port))
		print(str(threadNum) + 'ss connect successful')
		print(str(threadNum) + 'while conn')
	
		while 1:
			print("enter recv data")
			cdata = recv_data(threadNum, conn, ss, fake_ip, server_port)
			print("exit recv data")

			print("enter send to server")
			sdata = send_to_server(cdata, threadNum, conn, ss, fake_ip, server_port)
			print("exit send to server")

		
	except:
		print(str(threadNum) + 'uh oh cannot send client data to server')
		try:
			print(str(threadNum) + 'try reestablish connection to server')
			ss = socket.socket()
			fake_ip = FAKE_IP
			server_port = 8080
			print(str(threadNum) + 'connect proxy to server at server ip', fake_ip, ' port ', server_port)
			ss.connect((fake_ip, server_port))
			print(str(threadNum) + 'ss connect successful')
			print(str(threadNum) + 'while conn')

			print("enter recv data")
			cdata = recv_data(threadNum, conn, ss, fake_ip, server_port)
			print("exit recv dataaa")

			print("enter send to server")
			sdata = send_to_server(cdata, threadNum, conn, ss, fake_ip, server_port)
			print("exit send to server")
			
		
		except:
			print(str(threadNum) + 'cannot reestablish connection to server, break')
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
parser.add_argument('fake_ip')

args = parser.parse_args()
LOG, ALPHA, LISTEN_PORT, FAKE_IP, fake_ip = args.log, args.alpha, args.listen_port, args.fake_ip, args.fake_ip
print('finished parsing')
print(LOG, ALPHA, LISTEN_PORT, FAKE_IP, fake_ip)
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
