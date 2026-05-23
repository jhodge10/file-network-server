# Overview

This is a file network server that can list, upload, and downlaod files between seperate clinets that includes the server startup client. Pulling the code from github by cloning and changing the client.py to the hosts IP address will allow the server.py and client.py on seperate devices to connect and echange and view files.

The purpose of this software is to allow at least 2 users on different clients to be able to upload, download, and view the list of files that are in the server.

[Software Demo Video Networking](https://youtu.be/CmrbXwrnKxc)

# Network Communication

The architecture of the software is a client/server model.

TCP(Transmission Control Protocol) is used. The port number used was 5000 for the application. IP ports include 0.0.0.0, 127.0.0.1, and 10.36.40.192(IPv4 address)

The format of messages sent is by files that are uplaoded and downloaded between the client/server. You are able to upload images and .txt files and have information inside those files in order to have another way of communication.

# Development Environment

{Tools that were used include Virtual Machine Oracle Box (That did not end up being used in the final post), Git, Python, and VS Code}

{The language used on this project was Python.}

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Python TCP Server](https://medium.com/@mando_elnino/python-tcp-server-b945c68a983c)
* [Python HTTP servers](https://docs.python.org/3/library/http.server.html)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* I would like to improve the style of the server when someone accesses it. I want it to be on a web app and be able to style the look how I want.
* I would like to add a database to this as well. I want there to be information that is stored and saved across the server for anyone to be able to see and access other than the program.
* I want this to be easy to access rather than having to clone Github and setup like that. I want a server that starts up once the web app is started that closes when no one is using the site.
