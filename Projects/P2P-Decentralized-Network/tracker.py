from server import Server
from threading import Thread


class Tracker(object):
    PORT = 12000
    IP_ADDRESS = "127.0.0.1"

    def __init__(self,server):
        self.server = server
        self.swarm = []
        #Server.__init__(self,self.IP_ADDRESS,self.PORT)
    #swarm = ["age.txt"]
    def add_swarm(self,swarm):
        for i in self.swarm:
            if swarm.get_file_name() == i.get_file_name():
                return i
            else:
                self.swarm.append(swarm)
                return swarm
        self.swarm.append(swarm)
        return swarm
    
    def brodcast_peerIp(self,ip):
        self.server.send_to_all(ip)