#!/usr/bin/python3
import sys
import select
import time
import _thread
import os.path
from urllib.parse import urlparse
from socket import *


#use exceptions to process operator requests
class StopException(Exception):
	pass



#new thread to respond, but use keyline input to send something into a port directly


#zombie number relates to it's socket

#the personall tcp socket number is the zombie number


# upgrade to new thread
# figure out a way to use ALL


def socketManager():
	
	#set up command line input and list of sockets
	socketList = [0]
	for i in range(1, len(sys.argv)):
		print('opening port: ' + sys.argv[i])
		#get socket number from arguments
		socketPort = int(sys.argv[i])
		
		#set up requested socket
		serverSocket = socket(AF_INET, SOCK_STREAM)
		serverSocket.bind(('',socketPort))
		serverSocket.listen()
		print('port ', socketPort, ' is open and ready')
		
		#add to list
		socketList.append(serverSocket)
	
	
	#have a dictionary that keeps track of zombies and their sockets
	
	
	while True:
		try:
			#begin listening on all sockets
			readSockets, writeSockets, errSockets = select.select(socketList, [], [])
			
			
			for connectionsWithSockets in readSockets:
				
				
				if connectionsWithSockets == 0:
					#command line input
					data = str(sys.stdin.readline().strip())
					
					#parse operator commands here
					#have a dirrect inlet to sockets here
					#hijacks the tcp socket to send opperator message
					
					if (data == 'STOP') or (data == 'stop') or (data == 'Stop'):
						raise StopException
				else:
					#socket input
					clientConnectionSocket, addrIP = connectionsWithSockets.accept()
					print('Connection with', addrIP, 'over', clientConnectionSocket)
					#this function below is multithreaded
					_thread.start_new_thread(clientManager, (clientConnectionSocket, addrIP, ))
		
		
		except (KeyboardInterrupt, StopException):
			print('\n')
			for i in socketList:
				if i != 0:
					print('socketClosed')
					i.close()
			
			break
	
	return


def clientManager(clientConnectionSocket, addrIP):
	
	counter = 0
	print('a new thread has been started')
	while True:
		
		#buffer client request
		requestFromClient = ''
		while True:
			requestFromClient += clientConnectionSocket.recv(1024).decode()
			
			if requestFromClient.find('\rE\n') != -1:
				time.sleep(2)
				break
		
		
		
		print(repr(requestFromClient), '\n')
		
		
		if counter == 0:
			dataFromServer = ''
			dataFromServer = 'I\rQ\n1234\rE\n'
			clientConnectionSocket.send(dataFromServer.encode())
		
		
		#NEVER PUT TWO ENDINGS IN THE SAME MESSAGE
		
		dataFromServer = ''
		if counter == 0:
			dataFromServer = 'RO/1thru10.py\rA\nO/shouldFail.py\rE\n'
			
		elif counter == 1:
			dataFromServer = 'QO/1thru10.py\rA\nO/shouldFail.py\rE\n'
			
		elif counter == 2:
			dataFromServer = 'SO/1thru10.py\rA\nO/shouldFail.py\rE\n'
			
		else:
			dataFromServer = 'KO\rE\n'
		
		
		counter += 1
		
		#send data
		clientConnectionSocket.send(dataFromServer.encode())
		
	
	#close socket
	clientConnectionSocket.close()
	print('a thread has closed')
	#assumption: returning from a muli-threading function will kill the thread
	return


def main():
	
	#display ip
	print(gethostbyname(gethostname()))
	print('server opened')
	#start server
	socketManager()
	print('server closed')
	
	
main()
