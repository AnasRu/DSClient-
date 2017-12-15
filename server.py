import socket
import sys
import threading
from ctypes import py_object
from time import time
from unittest.mock import _ANY


class Client(threading.Thread):
    def __init__(self, ip, port, connection, clients, connectionpair):
        threading.Thread.__init__(self)
        self.connection = connection
        self.ip = ip
        self.port = port
        self.clients = clients
        self.connectiopair = connectionpair

    def send_to_all_clients(self, msg):
        connectedClients = self.clients
        for client in connectedClients :
            client.connection.send(msg)
    def properList(self,clients):
        clientlist = []
        for i in clients:
            clientlist.append(str(i.port))
        return clientlist
    def run(self):

        # print(connectionList)
        while True:
            connectionList = self.properList(self.clients)
            data = self.connection.recv(1024)

            print(connectionList)

            if data.decode() == 'all' :
                for i in self.clients:
                    print(i.ip, i.port)
            elif str(data.decode()) in connectionList:
                print('I get his')
                port = 0
                indexedClient = None
                for i in self.clients:
                    if str(i.port) == str(data.decode()):
                        print(self.connectiopair[str(i.port)])
                        print(self.clients)
                        port = i.port
                        indexedClient = i
                        break

                        # for j in self.clients:
                        #     if j.port == i.port:
                        #         index = self.clients.index(j)
                        #         self.clients.pop(index)
                        #         break
                        # self.connectiopair[str(i.port)].close()
                # connectionList.remove(str(port))
                self.connectiopair[str(port)].shutdown(socket.SHUT_RDWR)
                self.connection.close()
                self.clients.remove(indexedClient)

            else:# data:
              #  self.connection.sendall(data)
                self.send_to_all_clients(data)

            # else :
            #     break
        self.connection.close()


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.address = (self.ip, self.port)
        self.server = None
        self.clients = []
        self.connectionpair = {}

    # def send_to_client(self, ip, port, msg):
    #     for client in self.clients :
    #         if client.ip == ip and client.port == port :
    #             client.connection.send(msg)

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.address)
        except socket.error:
            if self.server:
                self.server.close()
            sys.exit(1)


    def run(self):
        self.open_socket()
        self.server.listen(5)

        while True :
            connection, (ip, port) = self.server.accept()
            self.connectionpair[str(port)] = connection
            c = Client(ip, port, connection, self.clients,self.connectionpair)
            self.clients.append(c)



            c.start()



        self.server.close()

if __name__ == '__main__':
    s = Server('127.0.0.1', 10000)
    s.run()
