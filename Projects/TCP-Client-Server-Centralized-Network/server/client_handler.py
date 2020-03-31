#######################################################################
# File:             client_handler.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle

from threading import Thread
import threading
import datetime
now = datetime.datetime.now()

lock = threading.Lock()

class ClientHandler(object):
    global lock
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        self.server.send_client_id(self.clientsocket, self.client_id)
        self.unreaded_messages = []
        self.chatrom_info = {}

  
    def clientSetUp(self):
       
       
        
        lock.acquire()
        
        
        while True:
            data = self.server.receive(self.clientsocket)
            if 'clientName' in data:
                self.clientName = data['clientName']
                self.server.setActiveClients(data['clientName'],self.client_id)
                self.server.setClients(self.client_id,self)
                
                
            if 'reqMenu' in data:
                self.server.send(self.clientsocket,{'showMenu':True})
                
                break

            if not data:
                return
        lock.release()
        self.process_options()




    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        while True:
            

            data = self.server.receive(self.clientsocket)
            print(data)
            if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6: # validates a valid option selected
                option = data['option_selected']
                if option == 1:
                    self._send_user_list()
                elif option == 2:
                    data = self.server.receive(self.clientsocket)
                    recipient_id = data['recipient_id']
                    message = data['message']
                    self._save_message(recipient_id, message)
                elif option == 3:
                    self._send_messages()
                elif option == 4:
                    self.name = data['name']
                    room_id = data['room_id']
                    self._create_chat(room_id)
                elif option == 5:
                    self.name = data['name']
                    room_id = data['room_id']
                    self._join_chat(room_id)
                elif option == 6:
                    self._disconnect_from_server()
                    break
            else:
                print("The option selected is invalid")

    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        data = self.server.getActiveClients()
        print(data)
        self.server.send(self.clientsocket,data)
    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        try:
            client_handler = self.server.getClients()
            client_handler = client_handler[int(recipient_id)]
            #print(now.year,'-',now.month, '-', now.day, now.hour, ':', now.minute)
            string = (str(now.year) +'-' +str(now.month) + '-' +  str(now.day) +  ' ' +str(now.hour) + ':' + str(now.minute) + ' ' + str(message)+ ' ' +"From: (" + str(self.clientName) + ")")
            client_handler.unreaded_messages.append(string)
            self.server.send(self.clientsocket,"Message Sent")
        except Exception as e:
            print(e)
            self.server.send(self.clientsocket,"User Not Found")

    def _send_messages(self):
        """
        TODO: send all the unreaded messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        self.server.send(self.clientsocket,self.unreaded_messages)

    def _create_chat(self, room_id):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        self.server.add_chatroom(room_id,self)
        self.chatroom(room_id)
        
    def chatroom(self,room_id):
        self.server.send(self.clientsocket, "Welcome to chat room " + str(room_id))
        self.server.send(self.clientsocket,"Please Wait For One More User ------") 
        
        users = self.server.get_chatroom()
        users = users[room_id]
        while True:
            if len(users) > 1:
                self.server.send(self.clientsocket, {'start': True})
                self.server.send(self.clientsocket, "User Joined " + str(self.clientName))
                self.chat_listen(room_id)
                break

    def chat_listen(self, room_id):
        while True:
            data = self.server.receive(self.clientsocket)
            print("Listen :" , data)
            msg = (str(self.name) + '> ' +data) 
            users = self.server.get_chatroom()
            users = users[room_id]
            if data == "quit":
                break
            for user in users:
                if(user != self):
                    user.server.send(user.clientsocket,msg)

            if not data:
                break
                
    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        users = self.server.get_chatroom()
        users = users[room_id]
        users.append(self)
        print(self.server.get_chatroom())
        self.chat_listen(room_id)
        

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """

        del self.server.clients[self.client_id]
        del self.server.activeClients[self.clientName]
        

    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        print("here")
        self.delete_client_data()
        self.server.serversocket.close()













