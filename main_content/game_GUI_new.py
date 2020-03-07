#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 00:17:46 2018

@author: zixinwang
"""

# the new game gui
import tkinter as tk
import tkinter.messagebox
import time

class gameGUI(tk.Tk):
    def __init__(self, state=None, me='', playmate='',start_time = 0, the_key = ""):
        tk.Tk.__init__(self,state=None, me='', playmate='',start_time = 0, the_key = "")
        
        self.state = state
        self.me = me
        self.playmate = playmate
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (drawer_frame,guesser_frame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("drawer_frame")
        
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
    def xy(self,event):
        self.lastx, self.lasty = event.x, event.y

    def addLine(self,event):
        self.canvas.create_line((self.lastx, self.lasty, event.x, event.y))
        self.lastx, self.lasty = event.x, event.y  
    
    def set_msg(self,in_msg):
        self.msg.set(in_msg)
        
    def get_msg(self):
        return self.keyword.get()
    
    def update_time_guesser(self):
        remaining= int(21 - (time.time() - self.start_time))
        if remaining != -1:
            self.time_var.set(remaining)
        else:
            if self.send():
                self.round = 2
            
        self.root.after(100, self.update_time_guesser)
        
    def update_time_drawer(self):
        remaining= int(21 - (time.time() - self.start_time))
        if remaining != -1:
            self.time_var.set(remaining)
        else:
            if self.send():
                self.round = 2
            
        self.root.after(100, self.update_time_drawer)
 
    def send(self):
        return tkinter.messagebox.showinfo("Time's up!","The correct answer is :dddd")
    
class drawer_frame(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()
    
#    def __init__(self, parent, controller):
#        tk.Frame.__init__(self, parent)
#        self.controller = controller
#        label = tk.Label(self, text="This is the start page", font=controller.title_font)
#        label.pack(side="top", fill="x", pady=10)
#        
#        button1 = tk.Button(self, text="Go to Page One",
#                            command=lambda: controller.show_frame("guesser_frame"))
#        button1.pack()
#        
#        #print ("check")
#        #define root
#        self.root.title = "Happy Drawing!"
#        self.root.geometry('400x500')
#        # set mainwindow
#        self.root.columnconfigure(0, weight=1)
#        self.root.rowconfigure(0, weight=1)
#        
#        #frame
#        self.time_frame = Frame(self.root)
#        self.point_frame = Frame(self.root)
#        self.msg_frame = Frame(self.root)
#        self.pic_frame = Frame(self.root)
#        self.key_frame = Frame(self.root)
#        self.button_frame = Frame(self.root)
#        
#        
#        #the time frame
#        #time variable 
#        self.time_var = IntVar()
#        self.update_time_drawer()
#        
#        #self.update_time()
#        self.time = Label(self.time_frame, textvariable = str(self.time_var))
#        self.time_prompt = Label(self.time_frame, text = "Time Remaining: ")
#        
#        #pack
#        self.time_prompt.pack(side = 'left')
#        self.time.pack(side = 'left')
#        
#        # the top frame (name)
#        #str variable
#        
#        self.name_var1 = StringVar()
#        self.name_var1.set(self.me) # temporary
#        self.name_var2 = StringVar()
#        self.name_var2.set(self.playmate) # temporary
#        self.ppl1 = Label(self.point_frame, textvariable = self.name_var1)
#        self.ppl2 = Label (self.point_frame, textvariable = self.name_var2)
#        
#        
#        #pack
#        self.ppl1.pack(side = 'left')
#        self.ppl2.pack(side = 'left')
#        
#        #msg_frame
#        self.msg = StringVar()
#        self.msg.set('Sample Messages')
#        self.chat_prompt = Label(self.msg_frame, text = "Message: ")
#        self.chat = Label (self.msg_frame, textvariable = self.msg)
#        
#        #pack
#        self.chat_prompt.pack(side = 'left')
#        self.chat.pack(side = 'left')
#        
#        # the pic_frame.1
#            
#        # canvas
#        self.canvas = Canvas(self.pic_frame, width=200, height=200)
#        
#        self.canvas.grid(column=0, row=0, sticky=('n','w','w','s'))
#        self.canvas.bind("<Button-1>", self.xy)
#        self.canvas.bind("<B1-Motion>",self.addLine)
#        #self.canvas.pack()
#        
#        # the key_frame.1
#        self.key = Label(self.key_frame, text = "Keyword: ")
#        self.word_var = IntVar()
#        self.word_var.set(self.the_key)
#        self.keyword = Label(self.key_frame, textvariable = self.word_var)
#        
#        #pack
#        self.key.pack(side = 'left')
#        self.keyword.pack(side = 'left')
#        
#        # the bottom frame
#        self.send_button = Button(self.button_frame, text = "Send",\
#                                        command = self.msg)
#        self.q_button = Button(self.button_frame, text = "Quit",\
#                                        command = self.root.destroy)
#        # pack 
#        self.send_button.pack(side = 'left')
#        self.q_button.pack(side = 'left')
#        
#        
#        # pack the frame
#        self.time_frame.pack()
#        self.point_frame.pack()
#        self.msg_frame.pack()
#        self.pic_frame.pack() 
#        self.key_frame.pack()
#        self.button_frame.pack()
#        
#        pass
    
class guesser_frame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("guesser_frame"))
        button1.pack()
        
        self.the_key = the_key
        
        #print ("check")
        root.title = "Happy Guessing!"
        root.geometry('400x500')
        
        #frame
        self.time_frame = Frame(root)
        self.point_frame = Frame(root)
        self.msg_frame = Frame(root)
        self.pic_frame = Frame(root)
        self.key_frame = Frame(root)
        self.button_frame = Frame(root)
        
        #setup time
        self.time = 0
        self.start_time = start_time
        
        #the time frame
        #time variable 
        self.time_var = IntVar()
        self.update_time_guesser()
        
        #self.update_time()
        self.time = Label(self.time_frame, textvariable = str(self.time_var))
        self.time_prompt = Label(self.time_frame, text = "Time Remaining: ")
        
        #pack
        self.time_prompt.pack(side = 'left')
        self.time.pack(side = 'left')
        #print ("check")
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
        
       #----------------------------------------------------------------------
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
       #----------------------------------------------------------------------
        
        # the bottom frame
        self.send_button = Button(self.button_frame, text = "Send",\
                                        command = self.send_msg)
        self.q_button = Button(self.button_frame, text = "Quit",\
                                        command = root.destroy)
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
        
    