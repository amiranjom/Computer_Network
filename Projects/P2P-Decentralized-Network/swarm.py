class Swarm(object):

    def __init__(self,fileName):
        self.peers = []
        self.fileName = fileName

    def add_peer(self, peer):
        self.peers.append(peer)

    def delete_peer(self, peer):
        self.peers.remove(peer)

    def get_peers(self):
        return self.peers

    def get_file_name(self):
    
        return self.fileName

