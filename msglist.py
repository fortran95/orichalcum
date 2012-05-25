# -*- coding: utf-8 -*-

from Tkinter import *
class message_list(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('阅读消息')
        self.createWidgets()
        
        # Center the Window and set it un-resizable.
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2) # calculate position x, y
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(0,0)
        
        self.set_message('hello')
        
        self.root.mainloop()
    def createWidgets(self):
        # Create Labels
        self.label1 = Label(self.root)
        self.label1['text'] = '发件人：'
        self.label1.grid(row=0,column=0)
        # Create Sender Selecting Menu
        userlist_var = StringVar(self.root)
        userlist_opts= ['user1@babeltower','user2@babeltower']
        userlist_var.set(userlist_opts[0])
        self.userlist = OptionMenu(self.root,userlist_var,*userlist_opts)
        self.userlist.grid(row=0,column=1,columnspan=2,sticky=N+S+W+E)
        # Create Message Box
        self.message = Text(self.root,width=50,height=20)
        self.message.config(state=DISABLED)
        self.message.grid(row=1,column=0,columnspan=3)
        # Create Navigate Button and Labels
        self.prevbutton = Button(self.root)
        self.prevbutton['text'] = '上一条'
        self.prevbutton.grid(row=2,rowspan=2,column=0,sticky=N+S+W+E)
        
        self.timelabel = Label(self.root)
        self.timelabel['text'] = '2012-12-21 00:00:00 GMT'
        self.timelabel.grid(row=2,column=1)
        
        self.poslabel = Label(self.root)
        self.poslabel['text'] = '(0/0)'
        self.poslabel.grid(row=3,column=1)
        
        self.nextbutton = Button(self.root)
        self.nextbutton['text'] = '下一条'
        self.nextbutton.grid(row=2,rowspan=2,column=2,sticky=N+S+W+E)
        # Create Emergency Exit button
        self.exitbutton = Button(self.root)
        self.exitbutton['text'] = '关闭窗口'
        self.exitbutton['bg'] = 'Red'
        self.exitbutton['fg'] = 'White'
        self.exitbutton.grid(row=4,column=0,columnspan=3,sticky=N+S+W+E)
        
        # Update the window.
        self.root.update_idletasks()
    def set_message(self,message):
        self.message.config(state=NORMAL)
        self.message.delete(1.0,END)
        self.message.insert(END,message)
        self.message.config(state=DISABLED)
        
    def select_user(self,event):
        self.userlist.post(event.x_root,event.y_root)
    
frmMessage = message_list()