# -*- coding: utf-8 -*-
from Tkinter import *

usertext = ''
class Editor(object):
    def __init__(self,master,receiver,account):
        self.label0 = Label(master)
        self.label0['text'] = '收信人'
        self.label0.grid(row=0,column=0)
        
        self.label1 = Label(master)
        self.label1['text'] = '选择账号'
        self.label1.grid(row=1,column=0)
        
        self.receiver = Label(master)
        self.receiver['text'] = receiver
        self.receiver.grid(row=0,column=1)
        
        self.account = Label(master)
        self.account['text'] = account
        self.account.grid(row=1,column=1)
        
        self.editor = Text(master)
        self.editor.grid(row=2,column=0,columnspan=2)
        
        def save(m=master):
            global usertext
            usertext = self.editor.get(1.0,END)
            m.quit()
        self.yes = Button(master)
        self.yes['text'] = '保存并发送'
        self.yes['command'] = save
        self.yes.grid(row=3,column=0,sticky=N+E+W+S)
        
        def cancel(m=master):
            global usertext
            usertext = False
            m.quit()
        self.no = Button(master)
        self.no['text'] = '取消'
        self.no['command'] = cancel
        self.no.grid(row=3,column=1,sticky=N+E+W+S)
        
        master.update_idletasks()
        

def inputbox(receiver,account):
    global usertext
    root = Tk()
    root.title("给 %s 发送信息" % receiver)
    app = Editor(root,receiver,account)
    
    w = root.winfo_width()
    h = root.winfo_height()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2) 
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(0,0)
    
    root.mainloop()
    
    root.destroy()
    
    return usertext

if __name__ == "__main__":
    print inputbox("receiver","account")