########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: TCP Server Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name:
# Student ID:
# Student Github Username:
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Program Running instructions:
#               python server.py  # compatible with python version 2
#               python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import socket
import pickle
from threading import Thread
import client_handler

class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10 # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port = 12000):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        MAX_NUM_CONN = 10
        self.serversocket.bind((self.host,self.port))
        self.serversocket.listen(MAX_NUM_CONN)

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        try:
            self._bind()
            print("Server listening at ip ", self.host, " / port ", self.port)
            
        except:
            self.serversocket.close()
            print("Server failed to listen!!!")

    def thread_client(self, clienthandler, addr):
        ch =  client_handler.ClientHandler(self,clienthandler,addr)
        data = ch.process_client_data()
        
        """
        #TODO: receive, process, send response to the client using this handler.
        :param clienthandler:
        :return:
        """
      #  while True:
       #     data = self.receive(clienthandler)
        #    if not data: break
         #   self.send(clienthandler,"The server got the message ")
          #  print("The server got the following message : ", data)
    
    
             
    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
               clienthandler, addr = self.serversocket.accept()
               clientid = addr[1]
               self._send_clientid(clienthandler,clientid)
               Thread(target=self.thread_client, args=(clienthandler,addr)).start()
            except:
               # handle exceptions here
               raise

    def _send_clientid(self, clienthandler, clientid):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        data = {'clientid': clientid}
        self.send(clienthandler,data)


    def send(self, clienthandler, data):
        serialezed_data = pickle.dumps(data) 
        clienthandler.send(serialezed_data)
        """
        # TODO: Serialize the data with pickle.
        # TODO: call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        
    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()

# main execution
if __name__ == '__main__':
    server = Server()
    server.run()











