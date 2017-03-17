#!/usr/bin/python
import socket
import sys
from check_pkg import *
from thread import *


HOST = ''  # Symbolic name, meaning all available interfaces
PORT = 10000  # Arbitrary non-privileged port
DIST = 'Jessie'  # Distribution name

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	logging.info('Socket created')

except socket.error:
	logging.info('Socket error')

repos = Repository()
logging.info('Initialized Repository...')

# Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	logging.info('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

logging.info('Socket bind complete')

# Start listening on socket
s.listen(10)
logging.info('Socket now listening')


# Function for handling connections. This will be used to create threads
def clientthread(conn):
	logging.info('starting clientthread...')

	while True:
		try:
			# Receiving from client
			data = conn.recv(1024)
			if data:
				logging.info('received data: {}'.format(data))
				if data == "#START#":
					reply = repos.get_packages(DIST)
					conn.sendall(reply + "#END#")
			else:
				pass

		except Exception as e:
			logging.info('clientthread Error: {}'.format(e))
			break

	conn.close()

if __name__ == '__main__':

	# now keep talking with the client
	while 1:
		try:
			# wait to accept a connection - blocking call
			conn, addr = s.accept()
			logging.info('Connected with ' + addr[0] + ':' + str(addr[1]))

			# start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			start_new_thread(clientthread, (conn,))
		except Exception as e:
			logging.info('main Error: {}'.format(e))
	s.close()