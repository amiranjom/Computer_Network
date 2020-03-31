#######################################################################################
# File:             menu.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly necesary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################
from threading import Thread

class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized ans sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self,client):
         self.client = client

    
    def set_client(self, client):
        self.client = client

    def show_menu(self):
        """
        TODO: 1. send a request to server requesting the menu.
        TODO: 2. receive and process the response from server (menu object) and set the menu object to self.menu
        TODO: 3. print the menu in client console.
        :return: VOID
        """
        self.client.send({'reqMenu':True})
        data = self.client.receive()
        if 'showMenu' in data:
             print(self.get_menu())
      

    def process_user_data(self):
        """
        TODO: according to the option selected by the user, prepare the data that will be sent to the server.
        :param option:
        :return: VOID
        """
        while True:
            option = self.option_selected()
            if 1 <= int(option) <= 6: # validates a valid option
                if int(option) == 1:
                    data = self.option1()
                    print("Users in server:")
                    print(data)
                elif int(option) == 2:
                    data = self.option2()
                    print(data)
                elif int(option) == 3:
                    data = self.option3()
                    for message in data:
                        print("Total Unread Messages : ", len(data))
                        print (data, "\n")
                elif int(option) == 4:
                    self.option4()
                    print(data)
                elif int(option) == 5:
                    data = self.option5()
                elif int(option) == 6:
                    data = self.option6()
                    break
                print(self.get_menu())
            # TODO: implement your code here
            # (i,e  algo: if option == 1, then data = self.menu.option1, then. send request to server with the data)
            else:
                print("Invalid Option")
                print(self.get_menu())


    def option_selected(self):
        """
        TODO: takes the option selected by the user in the menu
        :return: the option selected.
        """
        option = input("Your option <enter a number>: ")
        # TODO: your code here.
        return option

    def get_menu(self):
        menu = """\n****** TCP CHAT ******
-----------------------
Options Available:
1. Get user list
2. Sent a message
3. Get my messages
4. Create a new channel
5. Chat in a channel with your friends
6. Disconnect from server
"""
        # TODO: implement your code here
        return menu

    def option1(self):
        """
        TODO: Prepare the user input data for option 1 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 1.
        """
        self.client.send({'option_selected': 1})
        data = self.client.receive()
        return data

    def option2(self):
        """
        TODO: Prepare the user input data for option 2 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 2.
        """
        message = input("Enter your message:")
        recipient_id = input("Enter recipent id:")
        data = {'recipient_id': recipient_id, 'message': message}
        self.client.send({'option_selected': 2})
        self.client.send(data)
        data = self.client.receive()
        # Your code here.
        return data

    def option3(self):
        """
        TODO: Prepare the user input data for option 3 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 3.
        """
        self.client.send({'option_selected': 3})
        data = self.client.receive()
        return data

    def option4(self):
        """
        TODO: Prepare the user input data for option 4 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        
        data = input("Enter new chat room id:")
        self.client.send({'option_selected': 4,'room_id':data, 'name': self.client.clientName})
        self.start_chat(data)
      
        

    def start_chat(self,data):

        while True:
            data = self.client.receive()
            print(data)
            if data == 'quit':
                break
            if 'start' in data:
                data = self.client.receive()
                print(data)
                Thread(target=self.input_chat, args=()).start()
        

        
    def input_chat(self):
        
        while True:
            msg = input()
            self.client.send(msg)
            if msg == 'quit':
                break


    def option5(self):
        """
        TODO: Prepare the user input data for option 5 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = input("Enter Room Id: ")
        self.client.send({'option_selected': 5,'room_id':data, 'name': self.client.clientName})
        self.listen_chat()
        # Your code here.
        return data

    def listen_chat(self):
        print("Welcome To the Chat Room")
        Thread(target=self.input_chat, args=()).start()
        while True:
            data = self.client.receive()
            if data == 'quit':
                break
            print(data)
            
            

    def option6(self):
        """
        TODO: Prepare the user input data for option 6 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 6.
        """
        self.client.send({'option_selected': 6})
        data = {}
        data['option'] = 6
        # Your code here.
        return data
