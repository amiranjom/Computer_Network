# CSC645 Computer Networks
#TESTT
# Lab 8 Solution: peer.py
# Author: Jose Ortiz
# client and server files are from lab 2. However, the server supports multi-threading like in lab 4

import math
from server import Server
from tracker import Tracker
from threading import Thread
from client import Client
from swarm import Swarm
from PWP import PWP
import torrent_parser as tp
from requests import get
import bencoding
import hashlib
import uuid


class Peer(Server,Client):
    """
    In this part of the peer class we implement methods to connect to multiple peers.
    Once the connection is created downloading data is done in similar way as in TCP assigment.
    """
    SERVER_PORT = 5000
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010

    def __init__(self, server_ip_address='0.0.0.0'):
        """
        Class constructor
        :param server_ip_address: used when need to use the ip assigned by LAN
        """
        #Server.__init__(self)  # inherits methods from the server
        #Client.__init__(self)  # inherit methods from the client
        self.server_ip_address = server_ip_address

        self.id = uuid.uuid4()  # creates unique id for the peer

    def run_server(self):
        """
        Already implemented. puts this peer to listen for connections requests from other peers
        :return: VOID
        """
        try:
            # must thread the server, otherwise it will block the main thread
            Thread(target=self._run, daemon=True).start()
        except Exception as error:
            print(error)  # server failed to run

    # noinspection PyMethodMayBeStatic
    def _connect_to_peer(self, client_port_to_bind, peer_ip_address, peer_port=5000):
        """
        This method connects a client from this peer to another peer.
        :param client_port_to_bind: port to bind the client to have more control over the ports used by our P2P network
        :param peer_ip_address: the ip address of the peer
        :param peer_port: the port of the peer
        :return: True if the client connected to the Peer. Otherwise, returns False
        """
        client = Client()
        try:
            # binds the client to the ip address assigned by LAN
            client.bind('0.0.0.0', client_port_to_bind)  # note: when you bind, the port bound will be the client id
            Thread(target=client.connect_to_server, args=(peer_ip_address, peer_port)).start()  # threads server
            return True
        except Exception as error:
            print(error)  # client failed to bind or connect to server
            """
              Note that the following line does not unbind the port. Sometimes, once the socket is closed 
              The port will be still bound until WAIT_TIME gets completed. If you get the error: 
              "[Errno 48] Address already in use" 
              Then, go to your terminal and do the following to unbind the port:
                  lsof -i tcp:<client_port>
              Then copy the "pid" of the process, and execute the following
                  kill -i <pid>
              There are also other ways to unbind the port in code. Try the following line in the server file right 
              after you create the server socket
                  serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
              The above line only works sometimes depending on the system and how busy is your CPU.
            """
            client.close()
            return False

    def connect(self, peers_ip_addresses):
        """
        With this function this peer creates multiple clients that connect to multiple peers
        :param peers_ip_addresses: the ip addresses of the peers (their servers ip_addresses)
        :return: VOID
        """
        client_port = self.CLIENT_MIN_PORT_RANGE
        default_peer_port = self.SERVER_PORT
        for peer_ip in peers_ip_addresses:
            if client_port > self.CLIENT_MAX_PORT_RANGE:
                break
            if "/" in peer_ip:  # checks if the ip address includes ports
                # This part is good if your P2P supports sharing different files
                # Then the same peer can run different servers in the same machine
                ip_and_port = peer_ip.split("/")
                peer_ip = ip_and_port[0]  # the ip address of the peer
                default_peer_port = int(ip_and_port[1])  # the port of the peer
            if self._connect_to_peer(client_port, peer_ip, default_peer_port):
                # the client connected. incrementing the client port here prevents
                # wasting ports in the range of ports assigned if the client connection fails.
                client_port += 1
    
    def check_if_announcer(self):
        if(self.external_ip == self.tracker_ip):
            print("You're the Announce, Setting Up the Tracker")
            #init for the announce
            ##setting up the blocks and initbitfield and pieces and ready to send
            return True
        else:
            print("Peer: Connecting to announce Tracker")
            return False

    
    def parse_torrent(self,torrent_name):
        parsed_torrent = tp.parse_torrent_file(torrent_name)
        print("Torrent File " + torrent_name +
         " was parsed and the announce address is : " + parsed_torrent['announce'])
        tracker_ip_port = parsed_torrent['announce'].split(":")
        self.fileName = parsed_torrent['info']['name']
        self.tracker_ip = tracker_ip_port[0]
        self.tracker_port = tracker_ip_port[1]
        self.num_pieces = math.ceil(int(parsed_torrent['info']['length'])/int(parsed_torrent['info']['piece length']))
        info = bencoding.bencode(parsed_torrent['info'])
        hash = hashlib.sha1()
        hash.update(repr(parsed_torrent['info']).encode('utf-8'))
        self.info_hash = hash.digest()
        print(self.info_hash)
        self.external_ip = get('https://api.ipify.org').text


    def peer_handler(self,server,clientsocket,host,port):

        while True:
            data = server._receive(clientsocket)
            #First thing check for handshake Message
                #Compare it with the info_hash
                #If the same, setup the swarm for that specific file 
            if 'handshake' in data:
                print("Outside")
                if self.info_hash == data['handshake']['info_hash']:
                    print("Inside")

                    swarm = Swarm(self.fileName)
                    swarm = self.announce_tracker.add_swarm(swarm)
                    swarm.add_peer(host+":"+port)
                    print(swarm.peers)
                    
                    #Tracker PWP to be setup and the bitfield to be setup
                    #Create a data_structure in swarm to send back to peer
            if not data: break
            print(data)




    def run(self):
        #torrent_file = str(input("Enter the torrent file name with extension (.torrent): "))
        torrent_file = "age.torrent"
        self.parse_torrent(torrent_file)
        if(self.check_if_announcer()):
            #Start the Server
            server = Server(self.get_ip(),int(self.tracker_port))
            server._listen()
      
            #Create an Empty Tracker with Server Instance
                #Add the Swarm for the specific file to the tracker List
            self.announce_tracker = Tracker(server)    

            
            #Create the PWP Instance, Make sure you set all the bitfields to "You have the file"

            #Listening for a handShake Message from the clients (Threading)
                #Listening for request from peer to receive all the Peer Ips in the Swarm or Tracker
            while True:
                try:
                    # accept connections from outside
                    (clientsocket, address) = server.serversocket.accept()
                    # now do something with the clientsocket
                    # in this case, we'll thread the handler for each peer. peer <-> tracker (announce)
                    host,port = clientsocket.getpeername()
                    Thread(target=self.peer_handler, args=(server,clientsocket, host, port)).start()
                    
                    print("Peer Connectd: ", host,port)
                    data = {'peerId': address[1]}
                    server._send(clientsocket,data)
                    print("Peer: " + str(address[1]) + " just connected")
                except Exception as error:
                    print(error)


         

            #Create the Empty Swarm
                #Setting up a dic with status and upload speed to share to all users.
    
            print("Tracker Implementation")

        else:
            self.client_tracker = Client()
            self.client_tracker.connect_to_server(self.tracker_ip,int(self.tracker_port))

                #Handshake
            #Connect to the announce Ip address from torrent file
            
            #Send the handshake Message (Create Instance PWP)
            pwp = PWP(self.num_pieces)
            self.handshake_message = pwp.handshake(self.info_hash,self.client_tracker.get_peerId())
            self.client_tracker.send({'handshake': self.handshake_message})
            print(pwp.msg._bitfield)
            while True:
                pass
            
            #Request list of Ip addresses from announce tracker

            #Connect to all the given Ip addresses from the tracker
                #Send Handshake message to all the peers
                    #If Interested and other Peers not choked Download Starts
                    #

            #Status: Choke and Not Interested
            #Role: Leecher

            #Request a Piece (Broad) 
                #Resources to check the hash with the piece.
                #Check if we have all the pieces to become seeder.    
            print("Peer Implementation")



# testing
peer = Peer()
peer.run()

#print("Peer: " + str(peer.id) + " running its server: ")
#peer.run_server()
#print("Peer: " + str(peer.id) + " running its clients: ")
# Two ways of testing this:
#  Locally (same machine):
#      1. Run two peers in the same machine using different ports. Comment out the next two lines (only servers run)
#      2. Then run a third peer, executing the next two lines of code.
#  Using different machines
#      1. Run two peers in different machines.
#      2. Run a peer in this machine.
#peer_ips = ['127.0.0.1/7001', '127.0.0.1/7000']  # this list will be sent by the tracker in your P2P assignment
#peer.connect(peer_ips)

""" Output running this in the same machine """
# Peer: 6d223864-9cd7-4327-ad02-7856d636af66 running its server:
# Listening for new peers at 127.0.0.1/5000
# Peer: 6d223864-9cd7-4327-ad02-7856d636af66 running its clients:
# Client id 5001 connected to peer 127.0.0.1/7001
# Client id 5002 connected to peer 127.0.0.1/7000

""" Output running one peer in this machibe in the other two in different machines """
# Peer: 6f4e024e9-0265-47ba-a525-1c880a7a9a5d running its server:
# Listening for new peers at 10.0.0.248/5000
# Peer: f4e024e9-0265-47ba-a525-1c880a7a9a5d running its clients:
# Client id 5001 connected to peer 10.0.0.251/5000
# Client id 5002 connected to peer 127.0.0.242/5000
