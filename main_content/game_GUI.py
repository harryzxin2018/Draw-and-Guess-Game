#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 22:34:59 2018

@author: zixinwang
"""

#from chat_client_class import *

from tkinter import *
import tkinter.messagebox

from chat_utils import *
import threading

class gameGUI():
    
    def __init__(self,state = None, me = '', playmate= '', start_time = time.time()):
        # import chat system
        '''
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        '''
        #self.chat = chat.Client()
        #self.args = args
        
        # set the state
        self.words = ["bird","tree","tintin","snowy"]
        self.me = me
        self.playmate = playmate
        self.state = state
        self.round = 1
        self.time = 0
        self.start_time = start_time
        
        # the main window
        self.root = Tk()
        
        # define frame
        self.time_frame = Frame(self.root)
        self.point_frame = Frame(self.root)
        self.msg_frame = Frame(self.root)
        self.pic_frame = Frame(self.root)
        self.key_frame = Frame(self.root)
        self.button_frame = Frame(self.root)
        
        
        # the time frame
        #time variable 
        self.time_var = IntVar()
        self.update_time()
        self.time = Label(self.time_frame, textvariable = str(self.time_var))
        self.time_prompt = Label(self.time_frame, text = "Time Remaining: ")
        
        #pack
        self.time_prompt.pack(side = 'left')
        self.time.pack(side = 'left')
        
        # the top frame (name)
        #str variable
        
        self.name_var1 = StringVar()
        self.name_var1.set(self.me) # temporary
        self.name_var2 = StringVar()
        self.name_var2.set(self.playmate) # temporary
        self.ppl1 = Label(self.point_frame, textvariable = self.name_var1)
        self.ppl2 = Label (self.point_frame, textvariable = self.name_var2)
        
        
        #pack
        self.ppl1.pack(side = 'left')
        self.ppl2.pack(side = 'left')
        
        #msg_frame
        self.msg = StringVar()
        self.msg.set('Sample Messages')
        self.chat_prompt = Label(self.msg_frame, text = "Message: ")
        self.chat = Label (self.msg_frame, textvariable = self.msg)
        
        #pack
        self.chat_prompt.pack(side = 'left')
        self.chat.pack(side = 'left')
        # two states
        if self.state == "drawer":
            # the pic_frame.1
            
            
            # set mainwindow
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            
            # canvas
            self.canvas = Canvas(self.pic_frame, width=200, height=200)
            
            self.canvas.grid(column=0, row=0, sticky=('n','w','w','s'))
            self.canvas.bind("<Button-1>", self.xy)
            self.canvas.bind("<B1-Motion>",self.addLine)
            #self.canvas.pack()
            
            # the key_frame.1
            self.key = Label(self.key_frame, text = "Keyword: ")
            self.word_var = IntVar()
            self.word_var.set(random.choice(self.words))
            self.keyword = Label(self.key_frame, textvariable = self.word_var)
            
            #pack
            self.key.pack(side = 'left')
            self.keyword.pack(side = 'left')
          
        elif self.state == "guesser":
             # the pic_frame.2
            self.canvas = Canvas(self.pic_frame, width=300, height=300)
            self.canvas.pack()
            
            
            # the key_frame.2 
            self.key = Label(self.key_frame, text = "Your Guess: ")
            self.keyword = Entry(self.key_frame, width = 30) 
            self.result_var = IntVar()
            self.result_var.set("")
            self.result = Label(self.key_frame, textvariable = self.result_var)
        
            #pack
            self.key.pack(side = 'left')
            self.keyword.pack(side = 'left')
            self.result.pack(side = "left")
        
        # the bottom frame
        self.send_button = Button(self.button_frame, text = "Send",\
                                        command = self.msg)
        self.q_button = Button(self.button_frame, text = "Quit",\
                                        command = self.root.destroy)
        # pack 
        self.send_button.pack(side = 'left')
        self.q_button.pack(side = 'left')
        
        # pack the frame
        self.time_frame.pack()
        self.point_frame.pack()
        self.msg_frame.pack()
        self.pic_frame.pack() 
        self.key_frame.pack()
        self.button_frame.pack()
        
        
        #mainloop
        #self.root.mainloop()
        def set_msg(self):
            
            pass
            
        def return_msg(self):
            return
            pass
    '''   
    def comm(self):
        my_msg, peer_msg = self.get_new_msgs()
        if len(my_msg) > 0:
            msg = json.dumps({"action":"send", "answer":my_msg})
            print(msg)
            self.send(msg)
            response = json.loads(self.recv())
            if response["result"] == 'right':
                self.result_var.set("Right")
            elif response["result"] == 'wrong':
                self.result_var.set("Wrong")
                self.keyword.delete(0,END)
            
        else:               # fix: dup is only one of the reasons
           pass
     '''   
    def update_time(self):
        remaining= int(11 - (time.time() - self.start_time))
        if remaining != -1:
            remaining= int(11 - (time.time() - self.start_time))
            self.time_var.set(remaining)
        else:
            if self.send():
                self.round = 2
                self.word_var.set(random.choice(self.words))
                self.start_time = time.time()  
            
        self.root.after(100, self.update_time)
        
    def send(self):
        return messagebox.showinfo("Time's up!","The correct answer is :dddd")
    
    
        
    def run_gui(self): 
        pass
    '''
    def get_new_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        my_msg = self.get_keyword()
        
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg
    
    def get_keyword(self):
        return self.keyword.get()
    '''
    
# test
#mygui = gameGUI('drawer')
#mygui.root.mainloop()

