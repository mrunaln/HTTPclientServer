# Mrunal Nargunde
# Id - 800829282
# email - mnargund@uncc,edu
#!/usr/bin/env python 

import sys

""" 
A simple echo client 
""" 

import socket 

class client():

  def __init__(self):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      host = sys.argv[1] 
      port = sys.argv[2] 
      s.connect((host,int(port)))
      self.sendRequest(s)

  def sendRequest(self, socket):
      HTTPcommand = sys.argv[3]
      filePath = sys.argv[4]
      socket.send(HTTPcommand + " " + filePath + " HTTP/1.1\r\n\r\n") 

      size = 1024 
      data = socket.recv(size) 
      socket.close() 
      print 'Received:', data
  
client = client()
