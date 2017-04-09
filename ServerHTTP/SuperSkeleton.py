#import socket module 
from socket import *

#prepares a TCP/IP 
serverSocket = socket(AF_INET, SOCK_STREAM) 

#Binds socket to public host 
serverSocket.bind(('', 5555)) #socket is by any address visible in the same machine on port 5555
serverSocket.listen(1) #listens for 1 connection (1 client) 

while True: 
    #Establish the connection 
    print 'Ready to serve...' 
    connectionSocket, addr = serverSocket.accept() #accept connections from the outside 
    try:
        #(Outputs headers on different lines e.g. ) Message : GET /index.html HTTP1.1 \n Host.... 
        message = connectionSocket.recv(4096)  

        #takes message and splits on spaces and new lines into an array
                # Like this : ['GET', '/index.html', 'HTTP/1.1', 'Host:', ......
                # the [1] takes the second from array (e.g.) /index.html)
        #By default the Python function open opens file in text mode, meaning it will handle all input/output as text, while an image is decidedly binary.
        filename = message.split()[1]
        #####print filename

        #this opens the filename and gets rid of the slash (index.html)(Hello-World.png) 
        f = open(filename[1:])
        ####print filename[1:]

        #opens the contents of index.html or Hello-World.png
        outputdata = f.read() 

        # send one header line into socket
        # http://www.faqs.org/rfcs/rfc2616.html - protocols on how to send a message (include \r\n\r\n)
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")
	
        # Send the content of the requested file to the client 
        for i in range(0, len(outputdata)): 
            connectionSocket.send(outputdata[i]) 
        connectionSocket.send("\r\n")

        #closes file
        f.close()

        # Close the client connection socket
        connectionSocket.close() 

    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
        print "404 Not found"
        #taking the code from the index file and creating my own words for the error
        connectionSocket.send("<html><body>404 Not Found</body></html>")
	
    # Close the client connection socket
        connectionSocket.close()
    
serverSocket.close() 
