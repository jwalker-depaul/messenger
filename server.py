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
                # New client connected, store into collection
                clientPort = data[5:]
                self.clients[clientPort] = addr
                print self.clients
                
            print(data)

if __name__ == '__main__':
    server = Server()
    server.run()
