# Mrunal Nargunde
# Id - 800829282
# email - mnargund@uncc,edu
# Python Programming 

#!/usr/bin/env python 

""" 
A simple server 
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
  # Init called when the instance of server is created.
  # Default port = 60002 if no port specified
  def __init__ (self , port=60002):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    try :
        print "Lauching HTTP Server\n"
        self.s.bind(("localhost",port))
        #self.s.close()
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
      print "Shutting down the server\n"
      self.s.shutdown(socket.SHUT_RDWR)
    except Exception as e:
       print "Warning: Closing the socket "


  # Identify contentType from the file name
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
      return "image/jpeg"
    elif contentType[1] == "mp4":
      return "video/mpeg"
    elif contentType[1] == "mp3":
      return "audio/mpeg-3"
    else:
      return "text/plain"
 
  # generate headers depending on the code and filepath
  def generateHeaders(self,code, filepath):
    print "Constructing header\n"
    h =''
    if (code == 200):
      h = 'HTTP/1.1 200 OK' + CRLF
      h += 'Connection: keep-alive' + CRLF
    elif(code == 404):
      h = 'HTTP/1.1 404 Not Found'+ CRLF
      h += 'Connection: close' + CRLF
    
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
    h += 'Date: ' + current_date + CRLF
    h += 'Content-Type: ' + self.getContentType(filepath) + CRLF
    h += 'Server: Simple-Python-HTTP-Server' + "\n\n"
    return h

  # Listen for a request, Process the request from client, 
  # Generate a reponse and send it to client.
  def sendResponse(self,sock) :

   try: 
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
        filepath = data[1]
        filepath = filepath[1:]
        print filepath + "\n"
        contentType = filepath.split(".")
        if data[0] in validHTTPRequestGet:
              print "Handling GET Request "
            
              try:
                  HTTPresponse = ''
                  fileHandler = open(defaultPath+filepath,'rb')
                  content = fileHandler.read()
                  #fileHandler = open("../WebContent/iamsending.txt",'rb')
                  HTTPresponse = self.generateHeaders(200,  filepath) 
                  HTTPresponse +=  content
                  print " Found file. Sending file = " + filepath
                  client.send(HTTPresponse)
                  fileHandler.close()
              #If file not found then send 404 message
              except (OSError, IOError ) as e :
                  HTTPresponse = self.generateHeaders(404,  filepath) 
                  print "Warning : File " + filepath + " NOT Found. Sending error !"
                  fileHandler = open(defaultPath + "PagenotfoundGitHub.html",'rb')
                  content = fileHandler.read()
                  HTTPresponse +=  content
                  client.send(HTTPresponse)
                  fileHandler.close()
              client.close();
        
        
        elif data[0] in validHTTPRequestPut:
              print "Handling Put Request"
              #open file & write the contents in the file
              filepath = data[1]
              filepath = filepath[1:]
              contentType = filepath.split(".")

              try:
                fileHandler = open(defaultPath + "serverPut/" + filepath, 'wb')
                payload =  data[6]
                fileHandler.write(data[6])
                fileHandler.close()
                print "Writing successful closing socket"
                HTTPresponse =  "HTTP/1.1 201 Created"
                client.send(HTTPresponse)
                print "Sent response to client. Put Successful "
              except Exception as e :
                print "Exception while put  " 
                print e
              client.close();
        else:
            print  "Unknown HTTP Request method"
   # Handling graceful shutdown when on termination signal
   except KeyboardInterrupt:
       print "Keyboard interupt recieved gracefully handling this condition \n\n"
       self.shutdown()
       import sys
       sys.exit(0)


thisServer = server(60002)

