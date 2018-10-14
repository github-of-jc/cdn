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

# accept connections from clients
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