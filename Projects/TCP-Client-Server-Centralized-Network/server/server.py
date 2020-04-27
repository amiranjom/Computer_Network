#######################################################################
# File:             server.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################

from builtins import object
import socket
from threading import Thread
import threading
import pickle
from client_handler import ClientHandler
import sys, os


class Server(object):

    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=12007):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an INET, STREAMing socket
        self.host = ip_address
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {} # dictionary of clients handlers objects handling clients. format {clientid:client_handler_object}
        self.activeClients = {}
        # TODO: bind the socket to a public host, and a well-known port
        self.serversocket.bind((self.host,self.port))
        self.chat_rooms = {}


    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        try:
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server Listening at ", self.host, " and port : ", self.port)
            print(self.MAX_NUM_CONN)
        except:
            self.serversocke.close()
            print("Server failed to listen!!!")

    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                #TODO: Accept a client
                #TODO: Create a thread of this client using the client_handler_threaded class
                clientSocket, address = self.serversocket.accept()
                Thread(target=self.client_handler_thread, args=(clientSocket,address)).start()
            except:
                #TODO: Handle exceptions
                print("Error Occured, Raised")
                raise                


    def add_chatroom(self,room_id,user):
        self.chat_rooms[room_id] = []
        users = self.chat_rooms[room_id]            
        users.append(user)
        
    def get_chatroom(self):
        return self.chat_rooms
    def send(self, clientsocket, data):
        """
        TODO: Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return:
        """
        serialezed_data = pickle.dumps(data) 
        clientsocket.send(serialezed_data)


    def receive(self, clientsocket, MAX_BUFFER_SIZE=4096):
        
        """
        TODO: Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
        data = clientsocket.recv(MAX_BUFFER_SIZE)
        deserialezedData = pickle.loads(data)
        return deserialezedData

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        clientid = {'clientid': id}

        self.send(clientsocket, clientid)

    def setActiveClients(self,clientName,clientId):
        
        self.activeClients[clientName] = clientId
    
        print(self.activeClients)

    def setClients(self,clientId,clientHandler):
        
        self.clients[clientId] = clientHandler

        print(self.clients)

    def getActiveClients(self):

        return self.activeClients
    
    def getClients(self):
        return self.clients

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: void
        """

        #self.send_client_id(clientsocket,address[1])
        #TODO: create a new client handler object and return it
        clienthandler = ClientHandler(self,clientsocket,address)
        clienthandler.clientSetUp()
        
        """     
        lock = threading.Lock()
        lock.acquire()
        data = self.receive(clientsocket)

        if 'clientName' in data:

            self.activeClients[data['clientName']] = address[1]

            self.clients[address[1]] = clienthandler

            print(self.activeClients)
                
            self.send(clientsocket,{'showMenu':True})

            lock.release()
                 
            """

        
        


    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()


