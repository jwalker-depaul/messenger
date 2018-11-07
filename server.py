import socket
import sys

LOCAL_HOST = "127.0.0.1"
PORT = 1337
BUFF_SIZE = 1024

class Server:
    serverSocket = socket.socket()
    clients = {}
    ip = ""
    port = ""

    def __init__(self):
        # Setup UDP socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Setup UDP socket
        self.serverSocket.bind((LOCAL_HOST, PORT))

    def run(self):
        while True:
            # Recieve messages
            data, addr = self.serverSocket.recvfrom(BUFF_SIZE)
            if ("PORT=" in data):
                # New client connected
                self.addClient(data, addr)
            elif ("REMOVE_CLIENT=" in data):
                # Client is leaving
                self.removeClient(data, addr)
            else:
                # Regular message
                self.handleMessage(data, addr)

    def addClient(self, data, addr):
        # Add client to collection of clients
        clientPort = int(data[5:])
        self.clients[clientPort] = addr
        print self.clients

    def removeClient(self, data, addr):
        # Tell client to exit
        name = data[14:]
        self.serverSocket.sendto("CLIENT_EXIT", addr)

        # Remove client from collection and report
        self.handleMessage(name + " has left", addr) 
        del self.clients[addr[1]] # remove from dictionary
        print self.clients

    def handleMessage(self, data, addr):
        # Send message to everyone except the original sender
        for i in self.clients:
            if i != addr[1]:
                self.serverSocket.sendto(data, self.clients[i])
            
if __name__ == '__main__':
    server = Server()
    server.run()
