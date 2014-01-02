from socket import socket,AF_INET,SOCK_STREAM
import threading

class clientSckt(threading.Thread):
    
    HOST="127.0.0.1"
    PORT=1234
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def createConnection(self, Host=None, Port=None):
        HOST = Host
        PORT = Port
        if HOST==None: HOST = self.HOST
        if PORT==None: PORT = self.PORT
        
        ADDR = (self.HOST, self.PORT)
        
        self.sckt = socket( AF_INET,SOCK_STREAM)
        ##bind our socket to the address
        self.sckt.connect((ADDR))
        
    def send(self, data):
        return self.sckt.send(data)

    def close(self):
        return self.sckt.close()