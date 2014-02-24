Computer networks assignment -  Python

Learning - client server communication over HTTP/1.1

* Implementing Get request and Put request
  Server stores files from put request to location - HTTPclientServer/WebContent/serverPut/ 
  Server searches for files from get request from location - HTTPclientServer/WebContent/

* Run server from command line using:
    python server.py
* To run make the request from client use : 
    python client.py localhost 60001 Get /<filename>

  Supports file types :

    Images -
    png, jpg [Displayed in broswer]

    Audio files -
    mp3 [Downloads audio and can be played from the new location]

    Video -
    mp4 [Plays the video in browser]

    Text -
    plain text,html [Printed]
