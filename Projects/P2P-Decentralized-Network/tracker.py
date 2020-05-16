from server import Server
from threading import Thread


class Tracker(object):
    PORT = 12000
    IP_ADDRESS = "127.0.0.1"

    def __init__(self,server):
        self.server = server
        #Server.__init__(self,self.IP_ADDRESS,self.PORT)
"""
    def run(self):
        self._listen()
        while True:
            try:
                # accept connections from outside
                (clientsocket, address) = self.serversocket.accept()
                # now do something with the clientsocket
                # in this case, we'll pretend this is a threaded server
                Thread(target=self.client_thread, args=(clientsocket, address)).start()
                print("Client: " + str(address[1]) + " just connected")
            except Exception as error:
                print(error)
"""