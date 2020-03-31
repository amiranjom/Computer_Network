#######################################################################
# File:             client.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are 
#                   free to drop this client class, and add yours instead. 
# Running:          Python 2: python client.py 
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle

import sys, os
from menu import Menu


class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server 
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constractpr
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientid = 0
        
    def get_client_id(self):
        return self.clientid

    
    def connect(self):
        #self.host = input("Enter the server IP Address:")
        #self.port = input("Enter the server port:")

        self.host = "127.0.0.1"
        self.port = 12007
        self.clientName = input("Enter a name for your id: ")

        """
        TODO: Connects to a server. Implements exception handler if connection is resetted. 
	    Then retrieves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        try:
            self.clientSocket.connect((self.host,self.port))
            
            self.send({'clientName': self.clientName})

            print("Successfully connected to server with IP: ", self.host , "and port: ", self.port)
            
            while True: # client is put in listening mode to retrieve data from server.

                data = self.receive()

                if 'clientid' in data:

                        self.clientid = data['clientid']

                        print("Your Client Name is : ", self.clientName)

                        print("Your Client id is : ", self.clientid)
                        menu = self.getMenu()
                        #self.getUserSelection(menu)
                        menu.process_user_data()


                break


            #Call a method that takes user input
            
                

    
            
            self.close()

        except Exception as e:
            raise

    def getUserSelection(self,menu):
        while True:
            menu.process_user_data()
            print(menu.get_menu())
		
    def getMenu(self):

        menu = Menu(self)

        menu.show_menu()

        return menu
    

    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data) # serialized data
        self.clientSocket.send(data)

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        TODO: Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = self.clientSocket.recv(MAX_BUFFER_SIZE) # deserializes the data from server
        return pickle.loads(raw_data)
        

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()

		

if __name__ == '__main__':
    client = Client()
    client.connect()
