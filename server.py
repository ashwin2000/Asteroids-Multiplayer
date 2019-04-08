from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
class IM:
    
    def accept_incoming_connections(self):
        while True:
            client, client_address = self.SERVER.accept()
            print("%s:%s has connected." % client_address)
            client.sendall(bytes("Greetings from the cave! Now type your name and press enter!"))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()
    def handle_client(self,client):  
        name = client.recv(self.BUFSIZ).decode("utf8")
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        client.send(bytes(welcome ))
        msg = "%s has joined the team!" % name
        self.broadcast(bytes(msg ))
        self.clients[client] = name    
        while True:
            msg = client.recv(self.BUFSIZ)
            if msg != bytes("{quit}" ):
                self.broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}" ))
                client.close()
                del self.clients[client]
                self.broadcast(bytes("%s has left the team." % name ))
                break


    def broadcast(self,msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix )+msg)

    def __init__(self,port):        
        self.clients = {}
        self.addresses = {}

        self.HOST = ''
        self.PORT = port
        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.ADDR)

        
        self.SERVER.listen(5)
        print("Waiting for connection...")
        self.ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        self.ACCEPT_THREAD.start()
        self.ACCEPT_THREAD.join()
        self.SERVER.close()
