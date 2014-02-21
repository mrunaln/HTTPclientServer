# Mrunal Nargunde
# Id - 800829282
# email - mnargund@uncc,edu

#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket 
import time
import signal

defaultPath = "../WebContent/"
CRLF = "\r\n"
HTTPprotocol = "HTTP/1.1"
validHTTPRequestGet = ['Get','GET', 'get' ]
validHTTPRequestPut = [ 'Put', 'PUT', 'put' ]


class server():
  
  def __init__ (self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #FIXME port number should be taken from command line
    # Check port no is greater than 5000
    
    try :
        print "Lauching HTTP Server\n"
        self.s.bind(("localhost",60001))
    except Exception as e :
      print "ERROR - Failed to socket "
      self.shutdown()
      import sys
      sys.exit(1)

    print "Server successfully working activated\n"
    print "Press ctrl + c to shutdown and exit\n"
    self.sendResponse(self.s)


  def shutdown(self):
    try:
      print("Shutting down the server")
      self.socket.shutdown(socket.SHUT_RDWR)
    except Exception as e:
       print "Warning: could not shut down the socket. Maybe it was already closed ? "




  def getContentType(self,fileName):
    print "Constructing header\n"
    contentType = fileName.split(".")
    if contentType[1] == "html":
      return "text/html"
    elif contentType[1] == "txt":
      return "text/plain"
    elif contentType[1] == "xml":
      return "text/xml"
    elif contentType[1] == "css":
      return "text/css"
    elif contentType[1] == "png":
      return "image/png"
    elif contentType[1] == "jpg":
      return "image/jpg"
    elif contentType[1] == "mp4":
      return "video/mpeg"
    elif contentType[1] == "mp3":
      return "audio/x-mpeg-3"
    else:
      return "text/plain"
 

  def generateHeaders(self,code, filepath):
    print "Constructing header\n"
    if (code == 200):
      h = 'HTTP/1.1 200 OK' + CRLF
      h += 'Connection: keep-alive' + CRLF
    elif(code == 404):
      h = 'HTTP/1.1 404 Not Found'+ CRLF
      h += 'Connection: close' + CRLF

    current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
    h += 'Date: ' + current_date + CRLF
    h += 'Content-Type: ' + self.getContentType(filepath) + CRLF
    h += 'Server: Simple-Python-HTTP-Server' + CRLF + "\n\n"
    return h

  def sendResponse(self,sock) :

    while 1:
      print "Listening to request from client \n"
      sock.listen(1) 
      client, address = sock.accept() 
      size = 1025
      data = client.recv(size) 
      #Split the DATA to get the type of protocol
      data = data.split(" ")
      print "data = " + data[0] + " data [1] " + data[1] 
      # If Get then open the file and send the data 
      if data[0] in validHTTPRequestGet:
            print "Handling GET Request "
            filepath = data[1]
            filepath = filepath[1:]
            print filepath + "\n"
            contentType = filepath.split(".")
          
            try:
                fileHandler = open(defaultPath+filepath,'r')
                HTTPresponse = self.generateHeaders(200,  filepath) 
                HTTPresponse += CRLF + CRLF + fileHandler.read()
                print " Found file. Sending it !"
                client.send(HTTPresponse)
                fileHandler.close()
            #If file not found then send 404 message
            except (OSError, IOError ) as e :
                HTTPresponse = self.generateHeaders(400,  filepath) 
                print "Warning : File NOT Found. Sending error !"
                client.send(HTTPresponse)
            client.close();
      
      
      elif data[0] in validHTTPRequestPut:
            print "Handling Put Request"
            #If TEXT file then open file & write the contents in the file
            filepath = data[1]
            filepath = filepath[1:]
            contentType = filepath.split(".")

            try:
              fileHandler = open(defaultPath + "serverPut/" + filepath, 'w')
              payload =  data[6]
              #print "Writing " + data[6] + "to file"
              fileHandler.write(data[6])
              fileHandler.close()
              print "Writing successful closing socket"
              HTTPresponse = "HTTP/1.1 201 Created"
              client.send(HTTPresponse)
              print "Sent response to client. PUT SUCCESSFUL "
            except Exception as e :
              print "Exception while put  " 
              print e
            client.close();
      else:
            print  "Unknown HTTP Request method"
             

# Handling graceful shutdown when on termination signal
def graceful_shutdown(sig, dummy):
  print "Received an interupt: Shutting down "
  thisServer.shutdown()
  import sys
  sys.exit(0)

signal.signal(signal.SIGINT, graceful_shutdown)
thisServer = server()

