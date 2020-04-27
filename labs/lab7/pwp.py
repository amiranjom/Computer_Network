"""
Lab 7: Peer Wire Protocol (PWP)
Create a class with the basic implementation for the bitTorrent peer wire protocol
A basic template structure is provided, but you may need to implement more methods
For example, the payload method depending of the option selected
"""
import struct
from message import Message

class PWP(object):
    # pstr and pstrlen constants used by the handshake process
    PSTR = "BitTorrent protocol"
    PSTRLEN = 19
    CHOKE = 0
    UNCHOKE = 1
    INTERESTED = 2
    NOTINTERESTED = 3
    HAVE = 4
    BITFIELD = 5
    REQUEST = 6
    PIECE = 7
    CANCEL = 8
    PORT = 9
    # TODO: Define ID constants for all the message fields such as unchoked, interested....

    def __init__(self):
        self.message = Message()

    def handshake(self, info_hash, peer_id, pstrlen=PSTRLEN, pstr=PSTR):
        """
        TODO: implement the handshake
        :param options:
        :return: the handshake message
        """
        info_hash = info_hash.encode('utf-8')
        peer_id = peer_id.encode('utf-8')
        handshake_message =  struct.pack(
            '>B19s8x20s20s',
            pstrlen,                         # Single byte (B)
            b'BitTorrent protocol',     # String length 19 
                                        # 8 Tabs
            info_hash,                  # String length 20
            peer_id)
        
        return handshake_message


    def messages(self, len, message_id, payload):
        """
        TODO: implement the message
        :param len:
        :param message_id:
        :param payload:
        :return: the message
        """
        if message_id is self.BITFIELD:
            pass
        elif message_id is self.INTERESTED:
            print(Interested())
    
    
    def intersted(self):
        print("Here")
        

class Interested(object):
    """
    The interested message is fix length and has no payload other than the
    message identifiers. It is used to notify each other about interest in
    downloading pieces.
    Message format:
        <len=0001><id=2>
    """

    def encode(self) -> bytes:
        """
        Encodes this object instance to the raw bytes representing the entire
        message (ready to be transmitted).
        """
        return struct.pack('>Ib',
                           1,  # Message length
                           1)

    def __str__(self):
        return 'Interested'




if __name__ == '__main__':
    pwp = PWP()
    pwp.handshake("slsldkdkfjfjdkdjdkdj","slsldkdkfjfjdkdjdkdj")
    pwp.messages(1,2,1)