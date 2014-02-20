# Mrunal Nargunde
# Id - 800829282
# email - mnargund@uncc,edu

#!/usr/bin/env python 

""" 
A simple echo server 
""" 

import socket 
import time
CRLF = "\r\n"


class server():
  
  def __init__ (self):
    print "Logd : Lauching HTTP Server"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind(("localhost",60001)) 
    self.sendResponse(s)

  def getContentType(self,fileName):
    print "Logd : constructing header "
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
    else:
      return "text/plain"
  
  def generateHeaders(self,code, filepath):
    print "Logd : constructing header "
    if (code == 200):
      h = 'HTTP/1.1 200 OK' + CRLF
    elif(code == 404):
      h = 'HTTP/1.1 404 Not Found'+ CRLF

    current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
    h += 'Date: ' + current_date + CRLF
    h += 'Content-Type:' + self.getContentType(filepath);
    h += 'Server: Simple-Python-HTTP-Server' + CRLF
    h += 'Connection: close' + '\n\n' 
    # signal that the conection wil be closed after complting the request

    return h


  def sendResponse(self,sock) :

    print "Logd : sendResponse"
    while 1:
      sock.listen(1) 
      client, address = sock.accept() 
      size = 1025
      data = client.recv(size) 
      #Split the DATA to get the type of protocol
      data = data.split(" ")
      print "data = " + data[0] + " data [1] " + data[1] 
      # If Get then open the file and send the data 
      if data[0] == "GET" or data[0] == "Get" or data[0] == "get":
            print "Handling GET Request "
            filepath = data[1]
            filepath = filepath[1:]
            contentType = filepath.split(".")
          #  print filepath
          
            try:
                fileHandler = open(filepath,'r')
                HTTPresponse = self.generateHeaders(200,filepath) 
                HTTPresponse += CRLF + CRLF + fileHandler.read()
                print " Found file. Sending it !"
                client.send(HTTPresponse)
                fileHandler.close()
            #If file not found then send 404 message
            except (OSError, IOError ) as e :
                HTTPresponse = "HTTP/1.1 404 Not Found"+ CRLF + "Date: Fri, 31 Dec 1999 23:59:59 GM"+ CRLF + "Content-Type:" + contentType[1]
                print "Warning : File NOT Found. Sending error !"
                client.send(HTTPresponse)
            client.close();
      
      
      #If Put then ...
      elif data[0] ==  "PUT" or data[0] == "Put" or data[0] == "put":
            print "Handling Put Request"
            client.close();
     else:
       print  "Unknown HTTP Request method"
             



thisServer = server()
