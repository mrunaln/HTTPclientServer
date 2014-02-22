# Mrunal Nargunde
# Id - 800829282
# email - mnargund@uncc,edu
# Python programming 

#!/usr/bin/env python 


# Client.py 

import sys

""" 
A simple  client 
""" 

import socket 
CRLF = '\r\n'
HTTPprotocol = 'HTTP/1.1'
validHTTPRequestGet = ['Get','GET', 'get' ]
validHTTPRequestPut = [ 'Put', 'PUT', 'put' ]

class client():

  #Function called when instance of the class is created.
  def __init__(self):
      print "Connecting client to server"
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      #Check if 4 arguments are provided before starting all the process
      
      # Check if argument is localhost
      if sys.argv[1] and sys.argv[1] not in ['localhost']:
        print "Error: Please enter localhost as your first argument\n"
        sys.exit(0)
      
      # Check if port number is greater than 5000
      if sys.argv[2] and sys.argv[2] < 5000 :
        print "Error :" + sys.argv[2] + " is a reserved port\n. Please enter a port higher than 5000\n "
        sys.exit(0)
      
      # Check if valid http request 
      if sys.argv[3] and sys.argv[3] not in validHTTPRequestGet + validHTTPRequestPut :
        print "Error : Invalid HTTP Request method " + sys.argv[3] + "\n"
        sys.exit(0)
      
      # Check if file name is provided 
      # If file name is '/' then assuming user needs index.html
      if sys.argv[4] and sys.argv[4] in ['/']:
        sys.argv[4] = "/index.html"

      host = sys.argv[1] 
      port = sys.argv[2] 
      s.connect((host,int(port)))
      self.sendRequest(s)

  # Function called from init 
  # Sends the request to server
  def sendRequest(self, socket):
      print "Sending request to server\n"
      HTTPcommand = sys.argv[3]
      filePath = sys.argv[4]
      if HTTPcommand in validHTTPRequestGet :
          socket.send(HTTPcommand + " " + filePath + " "+  HTTPprotocol + CRLF + CRLF) 
          size = 1024 
          data = socket.recv(size) 
          socket.close() 
          print 'Received:', data
      elif HTTPcommand in validHTTPRequestPut:
          fileHandler = open("../WebContent" + filePath, "r")
          print "Reading data from file to send payload to server\n"
          payload = fileHandler.read()
          socket.send(
              HTTPcommand + " " + filePath + " "+  HTTPprotocol + CRLF + 
              "Host: my simple client\r\n" +
              "{ \r\n" +
              payload +
              "} " + CRLF
              )
          print "Sent data to server\n "
          size = 1024
          response = " "
          while True:
            response = socket.recv(size)
            if response != " ":
              break

          print "Response recieved from server = " + response
          socket.close()
      else:  
          print "Bad request"
          socket.close()
        


client = client()
