"""
Lab 8: peer.py
This file contains a basic template of the Peer class. In this lab, your job 
is to implement all the parts marked as TODO. Note that you don´t need to run
the code of this lab. The goal of this lab is to see how your logic works, and
therefore, to make sure that you understood how peers perform the downloading 
and uploading process in the network, and also which challenges you may encounter
when implementing those functionalities. 
"""
from server import Server
from client import Client
from threading import Thread
import threading

class Peer (Server):

    SERVER_PORT = 12000
    CLIENT_MIN_PORT_RANGE = 12001
    CLIENT_MAX_PORT_RANGE = 12010

    def __init__(self, server_ip_address):
        print(server_ip_address)
        Server.__init__(self,server_ip_address, self.SERVER_PORT)
        Client.__init__(self)
        self.run_server()


    def run_server(self):
        """
        Already implemented. puts this peer to listen for connections requests from other peers
        :return: VOID
        """
        Thread(target=self.run, args=()).start()


    def _connect_to_peer(self, client_port_to_bind, peer_ip_address):
        """
        TODO: Create a new client object and bind the port given as a
              parameter to that specific client. Then use this client
              to connect to the peer (server) listening in the ip
              address provided as a parameter
        :param client_port_to_bind: the port to bind to a specific client
        :param peer_ip_address: the peer ip address that
                                the client needs to connect to
        :return: VOID
        """
        try:
            clientNew = Client()
            
            #To be Implemented in the Client Class
            clientNew._bind(client_port_to_bind,peer_ip_address)
            clientNew.connect(peer_ip_address,client_port_to_bind)
        except:
            raise

    def connect(self, peers_ip_addresses=["127.0.0.1","127.0.0.1"]):
        """
        TODO: Initialize a temporal variable to the min client port range, then
              For each peer ip address, call the method _connect_to_peer()
              method, and then increment the client´s port range that
              needs to be bind to the next client. Break the loop when the
              port value is greater than the max client port range.

        :param peers: list of peer´s ip addresses in the network
        :return: VOID
        """
       
        min_port = self.CLIENT_MIN_PORT_RANGE
        max_port = self.CLIENT_MAX_PORT_RANGE
        for peer_Ip in peers_ip_addresses:
            try:
                if min_port == max_port:
                    break
                else:
                    Thread(target=self._connect_to_peer, args=(min_port, peer_Ip)).start()
                    min_port += 1  
            except Exception as e:
                min_port -= 1
                print(e)




