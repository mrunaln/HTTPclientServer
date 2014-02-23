Computer networks assignment -  Python

Learning - client server communication over HTTP/1.1

* Implementing Get request and Put request
  Server stores files from put request to location - HTTPlientServer/WebContent/serverPut/ 
  Server searches for files from get request from location - HTTPlientServer/WebContent/

* Run server from command line using:
    python server.py
* To run make the request from client use : 
    python client.py localhost 60001 Get /<filename>

  Supports file types :

    Images -
    png, jpg

    Audio files -
    mp3

    Video -
    mp4

    Text -
    plain text,html
