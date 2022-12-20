#!/usr/bin/python3
import sys
from urllib.parse import urlparse
from socket import *




class Buffer(object):
    

    buf = ""


    def bufferMessages(self,sock):
        bulk_buf = ""
        while True:
            #receiving from socket
            mod_buf = sock.recv(1024)

            #decoding the value and placing into self.buf
            self.buf = self.buf + mod_buf.decode()
            if(self.buf==None or len(self.buf)==0):
                return

            #checks errors
            error = self.buf.find(' 200 ')
            if(error == -1):
                error = self.buf.find('Date: ')
                e_Buffer = self.buf[9:error - 1]
                print('ERROR:', e_Buffer)
                return
            
            #finds carrier return
            index = self.buf.find('\r\n\r\n')
            if (index != -1):
                #bulk_buf is after HTTP req
                bulk_buf = bulk_buf + self.buf[index+4:]
                self.buf = self.buf[0:index+4]

                #getting content-length
                contentL_index = self.buf.find('Content-Length:') + 16
                if(contentL_index == 15):
                    contentL_index = self.buf.find('content-length:') + 16
                contentL = int(self.buf[contentL_index: self.buf.find('\r', contentL_index)])

                #if length of bulk_buf is greater than content-length
                if(len(bulk_buf) >= contentL):
                    return bulk_buf

def url_p(url_parse):
    print("running url_p function")
    serverName = urlparse(url_parse)
    
    print('found net location:', serverName.netloc)
    serverLoc = serverName.netloc
    if(serverName.netloc.find(':') != -1):
        serverLoc = serverName.netloc[:serverName.netloc.find(':')]
    
    serverIP = gethostbyname(serverLoc)
    print('found serverIP:', serverIP)


    #checks if there is a port, if not then use 80
    if(serverName.port == None):
        serverPort = 80
    else:
        serverPort = serverName.port
    print('found serverPort:', serverPort)
    
    return serverName, serverLoc, serverIP, serverPort
    

def writeFile(file, msg):
    #overwrites/writes new files
    print('writing file...')
    newFile = open(file, 'w')
    newFile.write(msg)
    print("Written in:", file)
    
    
def main():
    print('finding', str(sys.argv[1]), '...')

    #using the urlparse library to break down the url link
    url_parse = str(sys.argv[1])
    serverName, serverLoc, serverIP, serverPort = url_p(url_parse)

    #prepare the buffer
    b = Buffer()
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect((serverIP, serverPort))
    print('connection with', serverIP, 'on port', serverPort)

    #create an HTTP request
    dataReq = 'GET ' + serverName.path + ' HTTP/1.1\r\nUser-Agent: Wget/1.19.4 (linux-gnu)\r\nAccept: */*\r\nAccept-Encoding: identity\r\nHost: ' + serverLoc + '\r\nConnection: Keep-Alive\r\n\r\n'
    print(dataReq)
    
    sock.send(dataReq.encode())

        
    msg = b.bufferMessages(sock)
    if(msg==None or len(msg)==0):
        sock.close()
        return

    #making the file using terminal, grabs 3rd argument (position 2)
    file = str(sys.argv[2])
    writeFile(file, msg)
    
    #close socket
    sock.close()

main()
