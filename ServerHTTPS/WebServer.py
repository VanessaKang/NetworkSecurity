#import socket module 
from socket import *
import ssl

serverSocket = socket(AF_INET, SOCK_STREAM)

#------------------------------------------------
"""
Prepare a sever socket 
"""

#Starting from Python 2.7.9, it can be more flexible to use SSLContext.wrap_socket() instead.

##ssl.wrap_socket(serverSocket, keyfile='server.key', certfile='server.pem',
##                server_side=False,cert_reqs='CERT_REQUIRED', ssl_version='PROTOCOL_TLS',
##                ca_certs='server.pem', do_handshake_on_connect=True, suppress_ragged_eofs=True,
##                ciphers='AES128-SHA256')


#-----------------------------------------------
serverPort = 5555
# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))
# Listen to at most 1 connection at a time
serverSocket.listen(1)
#------------------------------------------------

#This is creating the new wrapped SSL socket ( the rest are defaults)
newSocket = ssl.wrap_socket(serverSocket, certfile = "server.pem", do_handshake_on_connect=True, ciphers = "AES256-SHA256")


while True: 
    #Establish the connection 
	print ('Ready to serve...') 
	connectionSocket, addr = newSocket.accept()
	try:
		message =  (connectionSocket.recv(1024)).decode('utf-8')
		filename = message.split()[1]

		f = open(filename[1:],'rb')
		outputdata = f.read()
		f.close()
		
		"""
		Send HTTP header line(s) into socket 
	/
	Note: With send(), strings must be encoded into utf-8 first using encode('utf-8') 
		"""
		connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')

        #Send the content of the requested file to the client 
		connectionSocket.send(outputdata)

		connectionSocket.send(b'\r\n')

 
		# Close the client connection socket
		connectionSocket.shutdown(SHUT_RDWR)
		connectionSocket.close() 

	except IOError: 
		"""
		Send response message for file not found
		"""
		connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
		connectionSocket.send(b'<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n')

		"""
		Close client socket 
		"""
		connectionSocket.shutdown(SHUT_RDWR)
		connectionSocket.close() 

newSocket.close() 
