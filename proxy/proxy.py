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
	ts = time.time()
	ismod = False
	modcdata = None
	chunk_name = None
	print("before conn.recv, ts = " + str(ts))
	packet = conn.recv(10000)
	#print(str(threadNum) + 'packet is: \n' + packet)
	cdata = cdata + packet
	get_loc = cdata.find('\n')
	extension_loc = cdata.find(' ', 4)
	if cdata[extension_loc-4:extension_loc] == ".f4m":
		ismod = True
		modcdata = cdata.replace(".f4m","_nolist.f4m", 1)
		f = open(str(threadNum)+"cdata_f4m.xml", "w")
		f.write(cdata)
		f.close()
		print(str(threadNum) + 'received cdata: ============================' + modcdata)
		return ismod, cdata, modcdata, ts, chunk_name
	elif cdata[5:8] == "vod":
		f = open(str(threadNum)+"cdata.xml", "w")
		print("========!!!!!!\n" + cdata[4:extension_loc])
		print(cdata[9:extension_loc])
		chunk_name = cdata[9:extension_loc]
		f.write(cdata)
		f.close()
		print(str(threadNum) + 'received cdata: ============================' + cdata)
		return ismod, cdata, modcdata, ts, chunk_name
	else:
		f = open(str(threadNum)+"cdata.xml", "w")
		print("========!!!!!!\n" + cdata[4:extension_loc])
		print(cdata[5:8])
		f.write(cdata)
		f.close()
		print(str(threadNum) + 'received cdata: ============================' + cdata)
		return ismod, cdata, modcdata, ts, chunk_name

def reg_send_to_server(chunk_name, logf, alpha, ts, cdata, threadNum, conn, ss, fake_ip, server_port):
	print("received ts: " + str(ts))
	print("alpha: " + str(alpha))
	tf = -1
	req_bitrate = -1
	avgtp = -1
	chunk_size = -1
	#throughput
	tp = -1
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
					#print(str(threadNum) + 'server packet is: \n' + packet)
					sdata = sdata + packet
				else:
					break
			tf = time.time()
			tdiff = tf-ts
			print("tf: " + str(tf))
			if len(sdata) > 0:
				#print(str(threadNum) + "server data is:===============================\n" +  sdata)
				print(str(threadNum) + 'trying to send client the server data')
				print("chunk size: " + str(len(sdata)))
				print("calculate throughout:")
				tp = len(sdata)/(tf-ts)
	
				logf.write(str(tf) + " " + str(tdiff) + " " + str(tp) + " " + str(avgtp) + " " + str(req_bitrate) + " " + str(fake_ip) + " " + str(chunk_name))

				print("throughput: " + str(tp))
				print("sdata:\n")
				f = open(str(threadNum)+"sdata.xml", "w")
				f.write(sdata)
				conn.send(sdata)
				print(str(threadNum) + 'successful sending server data to client')
				return tp

		except Exception as e:
			print("ERROR:" + str(e))
			print(str(threadNum) + 'uh oh cannot send cdata to server')
			try:
				print(str(threadNum) + 'try reestablish connection to server')
				ss = socket.socket()
				server_port = 8080
				print(str(threadNum) + 'connect proxy to server at server ip', fake_ip, ' port ', server_port)
				ss.connect((fake_ip, server_port))
				print(str(threadNum) + 'ss connect successful, not sending or receiving tho reg')
			except Exception as e:
				print("ERROR:" + str(e))
				print(str(threadNum) + 'cannot reestablish connection to server, break client connection')
				conn.close()
				
	else:
		print(str(threadNum) + 'client data is empty, break')

def mod_send_to_server(chunk_name, logf, alpha, ts, cdata, modcdata, threadNum, conn, ss, fake_ip, server_port):
	print("#$#$%!$%!#$% IN MODDDDDDD*&^(*(U")
	print(cdata)
	print(modcdata)
	print("received ts: " + str(ts))
	print("alpha: " + str(alpha))
	tf = -1
	req_bitrate = -1
	chunk_size = -1
	avgtp = -1
	#throughput
	tp = -1
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
					#print(str(threadNum) + 'server packet is: \n' + packet)
					sdata = sdata + packet
				else:
					break
			tf = time.time()
			tdiff = tf-ts
			print("tf: " + str(tf))
			if len(sdata) > 0:
				#print(str(threadNum) + "server data is:===============================\n" +  sdata)
				print(str(threadNum) + 'trying to send client the server data')
				print("chunk size: " + str(len(sdata)))
				print("calculate throughout:")
				tp = len(sdata)/(tf-ts)
				logf.write(str(tf) + " " + str(tdiff) + " " + str(tp) + " " + str(avgtp) + " " + str(req_bitrate) + " " + str(fake_ip) + " " + str(chunk_name))
				print("throughput: " + str(tp))
				print("sdata:\n")
				f = open(str(threadNum)+"modsdata.xml", "w")
				f.write(sdata)
				conn.send(sdata)
				print(str(threadNum) + 'successful sending server data to client')
				
				if "bitrate" in sdata:
					try:
						print(str(threadNum)+"=========================YES BITRATE")
						print(type(sdata))
						loc = sdata.find("bitrate")
						loc_list = []
						while loc != -1:
							print("loc: " + str(loc) + "\n len(sdata): " + str(len(sdata)))
							loc_list.append(loc)
							print(loc_list)
							print("look for in between " + str(loc+1) + " and end")
							loc = sdata.find("bitrate", loc+1)
							print(loc!=-1)
						print("final loc_list:\n" + str(loc_list))
						return loc_list, tp, tf, len(sdata)
					except Exception as e:
						print("ERROR:" + str(e))
						print("CAN'T FIND LOC")
				else:
					print(":C:C:C:C:C:C:C:CC:C:C:CC:C:CC:C:C:C:C:C:C:C:C:C:C:C:C:C:CC:C:C:C:C:C:C:C::CC:C:C:C:C:C:C")
				return loc, tp, tf, len(sdata)

		except Exception as e:
			print("ERROR:" + str(e))
			print(str(threadNum) + 'uh oh cannot send cdata to server')
			try:
				print(str(threadNum) + 'try reestablish connection to server')
				ss = socket.socket()
				server_port = 8080
				print(str(threadNum) + 'connect proxy to server at server ip', fake_ip, ' port ', server_port)
				ss.connect((fake_ip, server_port))
				print(str(threadNum) + 'ss connect successful, not sending or receiving tho reg')
			except Exception as e:
				print("ERROR:" + str(e))
				print(str(threadNum) + 'cannot reestablish connection to server, break client connection')
				conn.close()
				
	else:
		print(str(threadNum) + 'client data is empty, break')

def connect_client_to_server(logf, conn, addr, threadNum, s, port, LOG, alpha, FAKE_IP):
	print('=====================================beginning of thread=' + str(threadNum))
	tp = -1
	tf = -1
	chunk_size = -1
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
		loc_list = []
		while 1:
			print("enter recv data")
			ismod, cdata, modcdata, ts, chunk_name = recv_data(threadNum, conn, ss, fake_ip, server_port)
			print("ISMODISMODISMOD")
			print(ismod)
			print("exit recv data")
			print("in main loop ts: " + str(ts))
			
			if ismod:
				print("enter MOD send to server")
				loc_list, tp, tf, chunk_size = mod_send_to_server(chunk_name, logf, alpha, ts, cdata, modcdata, threadNum, conn, ss, fake_ip, server_port)
				print("========= \n tf: " + str(tf) + "\n chunksize: " + str(chunk_size
	))
				print("exit MOD send to server in try\n go into reg send")
				tp = reg_send_to_server(chunk_name, logf, alpha, ts, cdata, threadNum, conn, ss, fake_ip, server_port)
				print(str(threadNum) + "loc_list:")
				print(str(threadNum) + str(loc_list))
				print(str(threadNum) + "throughput")
				print(str(threadNum) + str(tp))
				print("exit reg send")
			else:
				print("enter send to server")
				tp = reg_send_to_server(chunk_name, logf, alpha, ts, cdata, threadNum, conn, ss, fake_ip, server_port)
				print("========= \n tf: " + str(tf) + "\n chunksize: " + str(chunk_size
	))
				print("exit send to server in try\nthroughput:" + str(tp))
		print("END OF THE CONNECTION")
		return tp, tf, chunk_size
		
	except Exception as e:
		print("ERROR:" + str(e))
		print(str(threadNum) + 'uh oh cannot send client data to server')
		try:
			print(str(threadNum) + 'try reestablish connection to server')
			ss = socket.socket()
			fake_ip = FAKE_IP
			server_port = 8080
			tp, tf, chunk_size = None, None, None
			print(str(threadNum) + 'connect proxy to server at server ip', fake_ip, ' port ', server_port)
			ss.connect((fake_ip, server_port))
			print(str(threadNum) + 'ss connect successful')
			print(str(threadNum) + 'while conn')

			print("enter recv data in except")
			ismod, cdata, modcdata, ts, chunk_name = recv_data(threadNum, conn, ss, fake_ip, server_port)
			print("ISMODISMODISMOD")
			print(ismod)
			if ismod:
				print("enter MOD send to server")
				loc_list, tp, tf, chunk_size = mod_send_to_server(chunk_name, logf, alpha, ts, cdata, modcdata, threadNum, conn, ss, fake_ip, server_port)
				print("========= \n tf: " + str(tf) + "\n chunksize: " + str(chunk_size
	))
				print("exit MOD send to server in try\n go into reg send")
				tp = reg_send_to_server(chunk_name, logf, alpha, ts, cdata, threadNum, conn, ss, fake_ip, server_port)
				print("exit reg send")
			else:
				print("enter send to server")
				tp = reg_send_to_server(chunk_name, logf, alpha, ts, cdata, threadNum, conn, ss, fake_ip, server_port)
				print("========= \n tf: " + str(tf) + "\n chunksize: " + str(chunk_size
	))
			print("exit send to server in except\nthroughput:" + str(tp))
			conn.close()
			print("return stuff to init connection")
			return tp, tf, chunk_size
		
		except Exception as e:
			print("ERROR:")
			print(e)
			print(str(threadNum) + 'cannot reestablish connection to server, break')
			conn.close()
			print("return stuff")
			tp, tf, chunk_size = None, None, None
			return tp, tf, chunk_size


def init_connection(logf, conn, addr, threadNum, s, port, LOG, ALPHA, FAKE_IP):
	print("init connection at =============================== threadNum: " + str(threadNum))
	tp = None
	tf = None
	chunk_size = None
	tp, tf, chunk_size = connect_client_to_server(logf, conn, addr, threadNum, s, port, LOG, ALPHA, FAKE_IP)
	print("tp, tf, chunk_size" + str(tp) + "\n" + str(tf) + "\n" + str(chunk_size))
	print("============================== end of init connection threadNum: " + str(threadNum))
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

print("open file")
logf = open(LOG, "w")


while True:
	print('=====================================beginning of client loop for thread=' + str(threadNum))
	print('# print conn, addr')
	conn, addr = s.accept()
	print('Connected by', addr)
	# open up connection with server
	# server socket
	print('created client connection')
	thread.start_new_thread(init_connection, (logf, conn, addr, threadNum, s, port, LOG, ALPHA, FAKE_IP,))
	logf.write("\n")
	threadNum = threadNum + 1
logf.close()
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
