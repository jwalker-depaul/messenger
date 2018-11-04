import socket
import sys
from threading import Thread

LOCAL_HOST = "127.0.0.1"
SERVER_PORT = 1337
BUFF_SIZE = 1024

# Check for input (Need name and port)
if (len(sys.argv) < 3):
    print("Please enter username and port")
    sys.exit(0)

class Client:
    # Socket setup
    clientSocket = socket.socket()
    port = ""
    name = ""
    recvThread = Thread()
    sendThread = Thread()
    
    def __init__(self):
        self.name = sys.argv[1]
        self.port = sys.argv[2]
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Setup UDP Socket
        self.clientSocket.bind((LOCAL_HOST, int(self.port)))
        self.clientSocket.sendto("PORT=" + self.port, (LOCAL_HOST, SERVER_PORT))
        
    def run(self):
        #Thread for recieve
        self.recvThread = Thread(target = self.recieveMessages)
        self.sendThread = Thread(target = self.sendMessages)
        
        # Start threads
        self.recvThread.start()
        self.sendThread.start()

        # Join threads
        self.recvThread.join()
        self.sendThread.join()
                         
    def sendMessages(self):
        while True:
            message = raw_input("")
            if message.lower() == "exit":
                # Tell server you're leaving
                self.clientSocket.sendto(("REMOVE_CLIENT=" + self.name), (LOCAL_HOST, SERVER_PORT))
                break
            else:    
                self.clientSocket.sendto((self.name + ": " + message), (LOCAL_HOST, SERVER_PORT))

    def recieveMessages(self):
        while True:
            data, addr = self.clientSocket.recvfrom(BUFF_SIZE)
            if (data == "CLIENT_EXIT"):
                break
            print data

if __name__ == '__main__':
    client = Client()
    client.run()
