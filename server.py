import socket
import sys

LOCAL_HOST = "127.0.0.1"
PORT = 1337
BUFF_SIZE = 1024

class Server:
    serverSocket = socket.socket()
    port = ""
    clients = {}

    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Setup UDP socket
        self.serverSocket.bind((LOCAL_HOST, PORT))

    def run(self):
        while True:
            # Recieve message
            data, addr = self.serverSocket.recvfrom(BUFF_SIZE)
            if ("PORT=" in data):
                # New client connected
                self.handleClient(data, addr)
            elif ("REMOVE_CLIENT=" in data):
                self.removeClient(data, addr)
            else:
                self.handleMessage(data, addr)

    def handleClient(self, data, addr):
        clientPort = int(data[5:])
        self.clients[clientPort] = addr
        print self.clients

    def removeClient(self, data, addr):
        name = data[14:]
        #Tell client to exit
        self.serverSocket.sendto("CLIENT_EXIT", addr)
        self.handleMessage(name + " has left", addr) 
        del self.clients[addr[1]] # remove from dictionary
        print self.clients

    def handleMessage(self, data, addr):
        for i in self.clients:
            if i != addr[1]:
                self.serverSocket.sendto(data, self.clients[i])
            
if __name__ == '__main__':
    server = Server()
    server.run()
