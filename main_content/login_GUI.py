#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 15:30:32 2018

@author: zixinwang
"""

from tkinter import *
from chat_client_class import *

      
class loginGUI(Client):
    
    def __init__(self,args):
        
        # import chat system
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        
        # the main window
        self.root = Tk()
        self.root.title("ICS Chat")
        
        
        # define frame
        self.top_frame = Frame(self.root,width = "200")
        self.mid_frame1 = Frame(self.root)
        self.mid_frame2 = Frame(self.root)
        self.bottom_frame = Frame(self.root)
        
        # the top frame
        self.greet_msg = Label(self.top_frame, text = "Welcome to ICS Chat!")
        
        #pack
        self.greet_msg.pack()
        
        # the mid_frame1
        self.prompt1 = Label(self.mid_frame1, text = "Username: ")
        self.username = Entry(self.mid_frame1, width = 15) 
        
        #pack
        self.prompt1.pack(side = 'left')
        self.username.pack(side = 'left')
        
        # the mid_frame2 
        self.prompt2 = Label(self.mid_frame2, text = "Password: ")
        self.password = Entry(self.mid_frame2, width = 15) 
        
        #pack
        self.prompt2.pack(side = 'left')
        self.password.pack(side = 'left')
        
        # the bottom frame
        self.log_button = Button(self.bottom_frame, text = "Log in",\
                                        command = self.chat_new)
        self.q_button = Button(self.bottom_frame, text = "Quit",\
                                        command = self.root.destroy)
        # pack 
        self.log_button.pack(side = 'left')
        self.q_button.pack(side = 'left')
        
        # pack the frame
        self.top_frame.pack()
        self.mid_frame1.pack()
        self.mid_frame2.pack()
        self.bottom_frame.pack()
        
    def launch(self):
        mainloop()
        
    def kill(self):
        self.root.destroy()
        
    def get_username(self):
        return self.username.get()
    
    def get_password(self):
        return self.password.get()
        
# -----------------------------------------------------------------------------
    def get_login_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        my_msg = self.get_username()
        self.kill()
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg
    
    def login(self):
        my_msg, peer_msg = self.get_login_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = json.dumps({"action":"login", "name":self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)

    def chat_new(self):
        self.init_chat()
        #print("check0")
        
        
        while self.login() != True:
            self.output()
        
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        #print("system1: ", self.system_msg)
        self.output()
       
        #print ("current state: ", self.sm.get_state())
        
        while self.sm.get_state() != S_OFFLINE:
            #print("check_proc")
            self.proc()
            #print("check_proc finished")
            #print(self.system_msg)
            self.output()
            time.sleep(CHAT_WAIT)
            
        self.quit()
        
        
        pass
    
   
    
#mygui = loginGUI()
