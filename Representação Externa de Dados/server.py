import socket

s = socket.socket()
host = "127.0.0.1"
port = 20205
s.bind((host, port))

s.listen(5)
while True:
   c, addr = s.accept()
   print("connection from", addr)
   data = c.recv(1024)
   if data: print( data)
   c.close()