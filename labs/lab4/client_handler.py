########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: Server support for multiple clients
# Goal: Learning Networking in Python with TCP sockets
# Student Name:
# Student ID:
# Student Github Username:
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Running instructions: This program needs the server to run. The server creates an object of this class.
#
########################################################################################################################
import threading
import pickle
import socket



class ClientHandler(object):
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """
    def __init__(self, server_instance, clienthandler, addr):
        """
        Class constructor already implemented for you.
        :param server_instance:
        :param clienthandler:
        :param addr:
        """
        self.clientid = addr[1] # the id of the client that owns this handler
        self.server_ip = addr[0]
        self.server = server_instance
        self.clienthandler = clienthandler

    def print_lock(self):
        return threading.Lock() # modify the return to return a the lock created

    def process_client_data(self):
        while True:
            data = self.clienthandler.recv(4096)
            deserialezedData = pickle.loads(data)
            if not data: break
            lock = self.print_lock()
            lock.acquire()
            print("Client #", self.clientid ," this message : ", deserialezedData)
            self.clienthandler.send(pickle.dumps("Server Got the Message"))
            lock.release()
