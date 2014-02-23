# Mrunal Nargunde
# Id - 800829282
# email - mnargund@uncc,edu
# Python programming 

#!/usr/bin/env python 


# Client.py 

import sys
import errno
from socket import error as socket_error

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
      print "Setting up socket to communicate from client to server\n"
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      
      #Check if 5 arguments are provided before starting all the process
      if len(sys.argv) < 5:
        print "Error : Number of commands not sufficient\n"
        sys.exit(0)

      # Check if argument is localhost
      elif sys.argv[1] and sys.argv[1] not in ['localhost']:
        print "Error: Please enter localhost as your first argument\n"
        sys.exit(0)
      
      # Check if port number is greater than 5000
      elif sys.argv[2] and sys.argv[2] < 5000 :
        print "Error :" + sys.argv[2] + " is a reserved port\n. Please enter a port higher than 5000\n "
        sys.exit(0)
      
      # Check if valid http request 
      elif sys.argv[3] and sys.argv[3] not in validHTTPRequestGet + validHTTPRequestPut :
        print "Error : Invalid HTTP Request method " + sys.argv[3] + "\n"
        sys.exit(0)
      
      # If file path given is / the server will return index.html which is default file
      # Handling done at server side

      host = sys.argv[1] 
      port = sys.argv[2]
      try:
        s.connect((host,int(port)))
        print "Connection from client to server is successfulli\n"
        self.sendRequest(s)
      except socket_error as error:
        print "Connection refused. Maybe server is not started ? \n"
        sys.exit(0)
  
  
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
