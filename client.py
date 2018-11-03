import socket
import sys

LOCAL_HOST = "127.0.0.1"
SERVER_PORT = 1337

# Check for input (Need name and port)
if (len(sys.argv) < 3):
    print("Please enter username and port")
    sys.exit(0)

class Client:
    # Socket setup
    clientSocket = socket.socket()
    port = ""
    name = ""
    
    def __init__(self):
        self.name = sys.argv[1]
        self.port = sys.argv[2]
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Setup UDP Socket
        self.clientSocket.bind((LOCAL_HOST, int(self.port)))

    def run(self):
        self.clientSocket.sendto("PORT=" + self.port, (LOCAL_HOST, SERVER_PORT))
        while True:
            message = raw_input("")
            self.clientSocket.sendto((self.name + ": " + message), ((LOCAL_HOST, SERVER_PORT))

        break
                         
    def sendMessages(self):
        pass

    def recieveMessages(self):
        pass

if __name__ == '__main__':
    client = Client()
    client.run()
