
from tkinter import *
import tkinter.messagebox
import time
import json
import threading
from chat_utils import *
import random


class gameGUI(Tk):
    
    def __init__(self,g_state=None,s = None, me='',playmate='',start_time = 0):
        Tk.__init__(self)#, state,me,playmate,start_time)

        self.s = s
        #self.geometry("400x550")
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.g_state = g_state
        self.me = me
        self.playmate = playmate
        self.words = ["deadline","Steve Jobs","iPhone","crocodile","cucumber","pizza","UFO","Iron Man","potato","hotpot","snake","tent","ring","hurricane","drum","scissors"\
            ,"final week","hot dog","dinosaur","mosquito","diamond","rainbow","harp","fence","piano","watermelon","potato chips","camera"]
        self.point = 0
        self.ppoint = 0
        self.round = 1


        self.frames = {}
        for F in (drawer,guesser):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew",padx=0, pady=0)
        #print (self.frames)
        if self.g_state == "drawer":
            self.show_frame("drawer")
        elif self.g_state == "guesser":
            self.show_frame("guesser")
        
        #set the key word
        self.the_key = "Tree"
        self.setkey()

        # set up time
        self.time = 0
        self.start_time = start_time

        self.update_time()
        
        self.lock = threading.Lock()

        receive_thread = threading.Thread(target=self.receive_msg)
        receive_thread.daemon = True
        receive_thread.start()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
    def update_time(self):
        self.remaining= int(31 - (time.time() - self.start_time))
        if self.remaining > -1:
            self.frames["guesser"].time_var.set(self.remaining)
            self.frames["drawer"].time_var.set(self.remaining)
        else:
            if self.g_state == "guesser":
                if self.frames["guesser"].send(self.the_key):
                    self.turn()
                    mysend(self.s, json.dumps({"action": "g_level", "from": self.me,"message":"timeout"}))
        self.after(100, self.update_time)
        
    def turn(self):
        self.setround()
        self.frames["guesser"].keyword.delete(0, END)
        self.frames["drawer"].clear()
        self.frames["guesser"].clear()
        self.frames["drawer"].canvas.config(width = "400", height = "300")
        self.frames["guesser"].canvas.config(width="400", height="300")
        #self.geometry("400x550")
        self.round += 1
        self.start_time = time.time()
        if self.g_state == "drawer":
            self.g_state = "guesser"
            self.show_frame("guesser")
        elif self.g_state == "guesser":
            self.g_state = "drawer"
            self.show_frame("drawer")
        self.setkey()
        
    def setround(self):
        self.frames["guesser"].round_var.set(self.round)
        self.frames["drawer"].round_var.set(self.round)
    
    def setkey(self):
        if self.g_state == "drawer":
            self.the_key = random.choice(self.words)
            #time.sleep(1)
            mysend(self.s, json.dumps({"action":"g_key", "from": self.me, "message":self.the_key}))
            self.frames["drawer"].word_var.set(self.the_key)
        
    def send_msg(self):
        my_msg = self.get_msg()
        #print(my_msg, self.the_key)
        self.frames["guesser"].keyword.delete(0, END)
        if len(my_msg) > 0:     # my stuff going out
            mysend(self.s, json.dumps({"action":"g_exchange", "from": self.me, "message":my_msg}))
            msg = "[" + self.me + "]" + my_msg
            self.show_msg(msg)
        if my_msg.lower() == self.the_key.lower():
            if self.frames["guesser"].success():
                mysend(self.s, json.dumps({"action": "g_level", "from": self.me, "message": "success"}))
                self.point += 1
                self.frames["guesser"].point_var1.set(self.point)
                self.frames["drawer"].point_var1.set(self.point)
                self.turn()
    
    def show_msg(self,msg):
        self.frames["drawer"].msg.set(msg)
        self.frames["guesser"].msg.set(msg)
    
    def destroy(self):   
        Tk.destroy(self)

    
    def get_msg(self):
        return self.frames["guesser"].get_msg()
        
    def receive_msg(self):
        self.lock.acquire()
        try:
           #print("received check")  
           while True:
                #print ("1: stuck?")
                peer_msg = myrecv(self.s)
                #print ("2: not stuck!")
                #print (peer_msg)
                peer_msg = json.loads(peer_msg)
                if len(peer_msg["message"]) > 0:
                    pass
                if peer_msg["action"] == "g_exchange" and len(peer_msg["message"]) > 0:    # peer's stuff, coming in
                    msg = "["+peer_msg["from"]+"]" + peer_msg["message"]
                    self.show_msg(msg)
                elif peer_msg["action"] == "g_key":
                    self.the_key = peer_msg["message"]
                elif peer_msg["action"] == "g_level":
                    self.turn()
                    if peer_msg["message"] == "success":
                        self.ppoint += 1
                        self.frames["drawer"].point_var2.set(self.ppoint)
                        self.frames["guesser"].point_var2.set(self.ppoint)
                elif peer_msg["action"] == "g_pic":
                    self.frames["guesser"].receive_msg(peer_msg["message"])
                elif peer_msg["action"] == "clear":
                    #print ("clear here")
                    self.frames["guesser"].clear()

        finally:
            self.lock.release()
        
class drawer(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.me = controller.me
        self.playmate = controller.playmate
        self.round = controller.round
        self.s = controller.s
        self.controller = controller
        #print(self.playmate)
        
        self.cord_list = []
        self.dur_time = 0
        
        #frame
        self.time_frame = Frame(self)
        self.point_frame = Frame(self)
        self.msg_frame = Frame(self)
        self.pic_frame = Frame(self)
        self.key_frame = Frame(self)
        self.button_frame = Frame(self)

        
        #round
        self.round_var = IntVar()
        self.round_var.set(self.round)
        self.round = Label(self.time_frame, textvariable = str(self.round_var),fg = "#6f6f6f",font = ("Avenir",16))
        self.round_prompt = Label(self.time_frame, text = "Round: ",fg = "#6f6f6f",font = ("Avenir",16))
        
        #pack
        self.round_prompt.pack(side = 'left',padx=5)
        self.round.pack(side = 'left')
        
        #self.update_time()
        self.time_var = IntVar()
        self.time = Label(self.time_frame, textvariable = str(self.time_var),fg = "#6f6f6f",font = ("Avenir",16))
        self.time_prompt = Label(self.time_frame, text = "Time Remaining: ",fg = "#6f6f6f",font = ("Avenir",16))
        
        #pack
        self.time.pack(side = 'right',padx=5)
        self.time_prompt.pack(side='right')
        
        # the top frame (name)
        #str variable
        
        self.name_var1 = StringVar()
        self.name_var1.set(self.me) # temporary
        self.name_var2 = StringVar()
        self.name_var2.set(self.playmate) # temporary
        self.ppl1 = Label(self.point_frame, textvariable = self.name_var1,fg = "#C12B67",font = ("Avenir",20))
        self.ppl2 = Label (self.point_frame, textvariable = self.name_var2, fg = "#C12B67",font = ("Avenir",20))

        self.point_var1 = IntVar()
        self.point1 = Label(self.point_frame, textvariable = str(self.point_var1),fg = "#C12B67",font = ("Avenir",20))
        self.point_var2 = IntVar()
        self.point2 = Label(self.point_frame, textvariable = str(self.point_var2),fg = "#C12B67",font = ("Avenir",20))

        #pack
        self.point1.pack(side = 'left')
        self.ppl1.pack(side = 'left')
        self.ppl2.pack(side = 'left')
        self.point2.pack(side = 'left')
        
        
        #msg_frame
        self.msg = StringVar()
        self.chat_prompt = Label(self.msg_frame, text = "Message: ",fg = "#6f6f6f",font = ("Avenir",16))
        self.chat = Label (self.msg_frame, textvariable = self.msg,fg = "#6f6f6f",font = ("Avenir",16))
        
        #pack
        self.chat_prompt.pack(side = 'left')
        self.chat.pack(side = 'left')
        
        # the pic_frame.1
        
        # canvas
        self.canvas = Canvas(self.pic_frame,width = 400, bd = 1,borderwidth = 2, highlightcolor = "red",relief='ridge',highlightthickness = 1,height = 300)

        self.canvas.grid(column=0, row=0, sticky=('n','w','e','s'))
        self.canvas.bind("<Button-1>", self.xy)
        self.canvas.bind("<B1-Motion>",self.addLine)
        #self.canvas.pack()
 
        # the key_frame.1
        self.key = Label(self.key_frame, text = "Keyword: ",fg = "#6f6f6f",font = ("Avenir",16))
        self.word_var = IntVar()
        self.word_var.set("")
        self.keyword = Label(self.key_frame, textvariable = self.word_var,fg = "#6f6f6f",font = ("Avenir",16))
        
        #pack
        self.key.pack(side = 'left')
        self.keyword.pack(side = 'left')
        
        # the bottom frame
        #self.send_button = Button(self.button_frame, text = "Send",\
                                        #command = self.msg)
        self.clear_button = Button(self.button_frame, text = "Clear", command = self.clear, fg = "#c12b67",bg="#FFFFFF", height=1, width=7,font = ("Avenir",14),relief=FLAT)
        self.q_button = Button(self.button_frame, text = "Quit",\
                                        command = controller.destroy, fg = "#c12b67",bg="#FFFFFF", height=1, width=7,font = ("Avenir",14),relief=FLAT)
        # pack 
        #self.send_button.pack(side = 'left')
        self.clear_button.pack(side = "left",padx=10, pady=5)
        self.q_button.pack(side = 'right',padx=10, pady=5)
        
        
         #pack the frame
        self.time_frame.pack(fill=BOTH, expand=True)
        self.point_frame.pack()
        self.msg_frame.pack()
        self.pic_frame.pack()
        self.key_frame.pack()
        self.button_frame.pack()

        def update(self):
            seself.update_idletasks()
            self.update()

 
    def xy(self, event=None):
        self.lastx, self.lasty = event.x, event.y
        self.cord_list += [event.x - 1, event.y - 1, event.x + 1, event.y + 1]  # the cordinates to "simulate" a dot

    
    def addLine(self, event=None):
        # start time
        start_time = time.time()

        # draw
        self.canvas.create_line((self.lastx, self.lasty, event.x, event.y), width=3)
        self.lastx, self.lasty = event.x, event.y

        #end_time
        end_time = time.time()
        self.dur_time += (end_time - start_time)
        #print(self.dur_time)

        # store data
        # alternative way: self.cord_list += [event.x, event.y]

        self.cord_list += [event.x - 1, event.y - 1, event.x + 1, event.y + 1]

        # buffer_time
        if self.dur_time >= 0.001:
            self.send_msg(self.cord_list)
            self.cord_list = []
            self.dur_time = 0 
            
    def send_msg(self, my_msg):
        # my stuff going out
        mysend(self.s, json.dumps({"action": "g_pic", "from": "[" + self.me + "]", "message": my_msg}))

    def clear(self):
        self.canvas.delete("all")
        self.controller.frames["guesser"].canvas.delete("all")
        mysend(self.s, json.dumps({"action": "clear", "from": "[" + self.me + "]", "message": "clear"}))

    def update(self):
        self.update_idletasks()
        self.update()

class guesser(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.me = controller.me
        self.playmate = controller.playmate
        self.round = controller.round
        self.s = controller.s
        parent.title = "Happy Guessing!"
        
        #frame
        self.time_frame = Frame(self)
        self.point_frame = Frame(self)
        self.msg_frame = Frame(self)
        self.pic_frame = Frame(self)
        self.key_frame = Frame(self)
        self.button_frame = Frame(self)

        # round
        self.round_var = IntVar()
        self.round_var.set(self.round)
        self.round = Label(self.time_frame, textvariable=str(self.round_var), fg="#6f6f6f", font=("Avenir", 16))
        self.round_prompt = Label(self.time_frame, text="Round: ", fg="#6f6f6f", font=("Avenir", 16))

        # pack
        self.round_prompt.pack(side='left', padx=5)
        self.round.pack(side='left')

        # self.update_time()
        self.time_var = IntVar()
        self.time = Label(self.time_frame, textvariable=str(self.time_var), fg="#6f6f6f", font=("Avenir", 16))
        self.time_prompt = Label(self.time_frame, text="Time Remaining: ", fg="#6f6f6f", font=("Avenir", 16))

        # pack
        self.time.pack(side='right', padx=5)
        self.time_prompt.pack(side='right')

        # the top frame (name)
        # str variable

        self.name_var1 = StringVar()
        self.name_var1.set(self.me)  # temporary
        self.name_var2 = StringVar()
        self.name_var2.set(self.playmate)  # temporary
        self.ppl1 = Label(self.point_frame, textvariable=self.name_var1, fg="#C12B67", font=("Avenir", 20))
        self.ppl2 = Label(self.point_frame, textvariable=self.name_var2, fg="#C12B67", font=("Avenir", 20))

        self.point_var1 = IntVar()
        self.point1 = Label(self.point_frame, textvariable=str(self.point_var1), fg="#C12B67", font=("Avenir", 20))
        self.point_var2 = IntVar()
        self.point2 = Label(self.point_frame, textvariable=str(self.point_var2), fg="#C12B67", font=("Avenir", 20))
        
        #pack
        self.point1.pack(side = 'left')
        self.ppl1.pack(side = 'left')
        self.ppl2.pack(side = 'left')
        self.point2.pack(side = 'left')

        # msg_frame
        self.msg = StringVar()
        self.chat_prompt = Label(self.msg_frame, text="Message: ", fg="#6f6f6f", font=("Avenir", 16))
        self.chat = Label(self.msg_frame, textvariable=self.msg, fg="#6f6f6f", font=("Avenir", 16))

        #pack
        self.chat_prompt.pack(side = 'left')
        self.chat.pack(side = 'left')
        
       #----------------------------------------------------------------------
        # the pic_frame.2
        self.canvas = Canvas(self.pic_frame, width=400, bd=1, borderwidth=2, highlightcolor= "green",relief='ridge', highlightthickness=1,
                             height=300)

        self.canvas.grid(column=0, row=0, sticky=('n','w','e','s'))

        # the key_frame.2 
        self.key = Label(self.key_frame, text = "Your Guess: ",fg="#6f6f6f", font=("Avenir", 16))
        self.keyword = Entry(self.key_frame, fg="#c12b67", font=("Avenir", 16))
        self.result_var = IntVar()
        self.result_var.set("")
        self.result = Label(self.key_frame, textvariable = self.result_var, fg="#6f6f6f", font=("Avenir", 16))
    
        #pack
        self.key.pack(side = 'left')
        self.keyword.pack(side = 'left')
        self.result.pack(side = "left")
       #----------------------------------------------------------------------

        # the bottom frame
        # self.send_button = Button(self.button_frame, text = "Send",\
        # command = self.msg)
        self.send_button = Button(self.button_frame, text="Send", command=controller.send_msg, fg="#c12b67", bg="#FFF",
                                   height=1, width=7, font=("Avenir", 14), relief=FLAT)
        self.q_button = Button(self.button_frame, text="Quit", \
                               command=controller.destroy, fg="#c12b67", bg="#FFF", height=1, width=7,
                               font=("Avenir", 14), relief=FLAT)
        # pack
        # self.send_button.pack(side = 'left')
        self.send_button.pack(side="left", padx=10, pady=5)
        self.q_button.pack(side='right', padx=10, pady=5)
        
        
        # pack the frame
        self.time_frame.pack(fill=BOTH, expand=True)
        self.point_frame.pack()
        self.msg_frame.pack()
        self.pic_frame.pack()
        self.key_frame.pack()
        self.button_frame.pack()
        
    def receive_msg(self,msg):
        # ---------receiving-----------------
        # a = time.time()
        # print("before receieved")

        # b = time.time()
        # print("after received, gap:", b - a)
        # ---------------------------------------


        # ----------processing----------------
        # c = time.time()
        #
        # print("before process")

        for i in range(0, len(msg), 4):
            cords = tuple(msg[i:i + 4])
            self.canvas.create_oval(cords, fill="black")

                # self.canvas.create_line(cords,width = 3)

            # alternative: self.canvas.create_line(msg)
            # f = time.time()
            # print("after draw, gap: ", f - e)


        # peer_msg = json.loads(peer_msg)
        # msg = peer_msg["message"]

        # msg = tuple(pre+post)

        # d = time.time()
        # print("after process, gap:", d - c)
        # ----------------------------------

        # ------------drawing-------------------------------
        # e = time.time()
        # print("before draw")
        
    def set_msg(self,in_msg):
        self.msg.set(in_msg)
        
    def get_msg(self):
        return self.keyword.get()
    
    def send(self,key):
        return tkinter.messagebox.showinfo("Time's up!","The correct answer is {}".format(key))

    def success(self):
        return tkinter.messagebox.showinfo("Time's up!", "You got it right!")

    def clear(self):
        self.canvas.delete("all")

    def update(self):
        self.update_idletasks()
        self.update()

if __name__ == "__main__":
    #game = gameGUI(None,"chuyi","tintin",int(time.time()),"snowy")
    #game.mainloop()   
    pass
    
        