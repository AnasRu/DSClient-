import socket
import sys

port = 10000
size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.connect(('127.0.0.1', port))
except socket.error as message:
    if s:
        s.close()
    print ("Could not open socket: " + message)
    sys.exit(1)

while True:
    data = input('> ')
    s.sendall(data.encode())

    data = s.recv(size)
    print("Server sent: %s " % data.decode())
s.close()
