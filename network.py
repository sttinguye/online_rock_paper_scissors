import socket
import pickle #send the whole object


class Network:
    def __init__(self):  # / initialize
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # /  create socket
        self.server = '157.245.193.101'
        self.port = 5555  # / open port
        self.addr = (self.server, self.port)  # / store server and port to address
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)  # / try to connect
            return self.client.recv(2048).decode()  # / check if connect or not
        except:
            pass

    def send(self, data):  # / send data
        try:
            self.client.send(str.encode(data)) #compose data
            return pickle.loads(self.client.recv(2048)) #received object
        except socket.error as e:
            print(e)
