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
    # Client info
    clientSocket = socket.socket()
    port = ""
    name = ""

    # Threads
    recvThread = Thread()
    sendThread = Thread()
    
    def __init__(self):
        # Grab info from cla
        self.name = sys.argv[1]
        self.port = sys.argv[2]

        # Setup UDP socket
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.bind((LOCAL_HOST, int(self.port)))

        # Notify server of client join
        self.clientSocket.sendto("PORT=" + self.port, (LOCAL_HOST, SERVER_PORT))
        self.clientSocket.sendto(self.name + " has come to chat!", (LOCAL_HOST, SERVER_PORT))
        
    def run(self):
        # Setup threads
        self.recvThread = Thread(target = self.receiveMessages)
        self.sendThread = Thread(target = self.sendMessages)
        
        # Start threads
        self.recvThread.start()
        self.sendThread.start()

        # Join threads
        self.recvThread.join()
        self.sendThread.join()
                         
    def sendMessages(self):
        while True:
            # Read in message from command line
            message = raw_input("")
            if message.lower() == "exit":
                # Tell server you're leaving
                self.clientSocket.sendto(("REMOVE_CLIENT=" + self.name), (LOCAL_HOST, SERVER_PORT))
                break
            else:    
                # Just send it bro
                self.clientSocket.sendto((self.name + ": " + message), (LOCAL_HOST, SERVER_PORT))

    def receiveMessages(self):
        while True:
            # Receive from server
            data, addr = self.clientSocket.recvfrom(BUFF_SIZE)
            if (data == "CLIENT_EXIT"):
                # Kill the thread
                break

            # Print messages from other users
            print data

if __name__ == '__main__':
    client = Client()
    client.run()
