"""
Lab 9: Routing and Handing
Implement the routing and handling functions
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
        self.routing_table = {[]}


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
        :param peer_ip_address: the peer ip address that the client needs to connect to
        :return: VOID
        """
        try:
            clientNew = Client()
            
            #To be Implemented in the Client Class
            clientNew._bind(client_port_to_bind,peer_ip_address)
            clientNew.connect(peer_ip_address,client_port_to_bind)
        except:
            raise

    def connect(self, peers_ip_addresses):
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
                    self.handling_clients(min_port,peer_Ip)
                    min_port += 1  
            except Exception as e:
                min_port -= 1
                print(e)



    def handling_clients(self, min_port, peer_Ip):
        """
        TODO: handle main services that a specific client provides such as threading the client....
        :param client:
        :return:
        """
        Thread(target=self._connect_to_peer, args=(min_port, peer_Ip)).start()

    def routing(self, piece, file_id, swarm_id, peer_id):
        """
        TODO: route a piece that was received by this peer, then add that piece to the routing table
        :param piece:
        :param file_id:
        :param swarm_id:
        :return:
        """

        if peer_id in self.routing_table:
            self.routing_table[peer_id] = [{"file_id": file_id,"swarm_id": swarm_id,"piece": piece}]
        else:
            self.routing_table[peer_id].append({"file_id": file_id,"swarm_id": swarm_id,"piece": piece})

