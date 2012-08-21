# -*- coding: utf-8 -*-
from Tkinter import *
import online

usertext = ''
usexi    = False
class Editor(object):
    def __init__(self,master,receiver,account,xi,userstat):
        global usertext,usexi
        usertext = ''
        usexi    = False

        self.label0 = Label(master,anchor=E)
        self.label0['text'] = '收信人:'
        self.label0.grid(row=0,column=0,padx=10,pady=2,sticky=N+E+W+S)
        
        self.label1 = Label(master,anchor=E)
        self.label1['text'] = '选择账号:'
        self.label1.grid(row=1,column=0,padx=10,pady=2,sticky=N+E+W+S)
        
        self.receiver = Label(master,anchor=W)
        self.receiver['text'] = receiver
        self.receiver.grid(row=0,column=1,columnspan=1,sticky=N+E+W+S)

        self.recstatus = Label(master,anchor=W)
        def refreshstat(m=master,u=userstat):
            olstate = online.get_status(u[0],u[1])

            if   olstate == -2:
                self.recstatus.config(text='当前离线',fg='#950')
            elif olstate == -1:
                self.recstatus.config(text='离开很久了',fg='#C90')
            elif olstate == 0:
                self.recstatus.config(text='信号不好',fg='#6A0')
            elif olstate == 1:
                self.recstatus.config(text='当前在线',fg='#0A0')
            else:
                self.recstatus.config(text='无法获取连通状态',fg='#F00')

            m.after(3300,refreshstat)
        master.after(0,refreshstat)
        self.recstatus.grid(row=0,column=2,sticky=N+E+W+S)
        
        self.account = Label(master,anchor=W)
        self.account['text'] = account
        self.account.grid(row=1,column=1,columnspan=2,sticky=N+E+W+S)
        
        self.editor = Text(master)
        self.editor.grid(row=2,column=0,columnspan=3)
        
        def save(m=master,u=False):
            global usertext,usexi
            usertext = self.editor.get(1.0,END)
            usexi    = u
            m.quit()
        def save_usexi(m=master):
            save(m,True)

        self.yes = Button(master)
        if xi:
            self.yes['state'] = DISABLED
            self.yes['text']  = '已选择禁止非密发送'
        else:
            self.yes['text'] = '直接发送'
        self.yes['command'] = save
        self.yes.grid(row=3,column=0,sticky=N+E+W+S)

        self.yes_xi = Button(master,bg='#F00',fg='#FFF')
        self.yes_xi['text'] = '加密并发送'
        self.yes_xi['command'] = save_usexi
        self.yes_xi.grid(row=3,column=1,sticky=N+S+W+E)
        
        def cancel(m=master):
            global usertext
            usertext = False
            m.quit()
        self.no = Button(master)
        self.no['text'] = '取消'
        self.no['command'] = cancel
        self.no.grid(row=3,column=2,sticky=N+E+W+S)
        
        master.update_idletasks()
        

def inputbox(receiver,account,xi,onlinestate):
    global usertext,usexi
    root = Tk()
    root.title("给 %s 发送信息" % receiver)
    app = Editor(root,receiver,account,xi,onlinestate)
    
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
    
    try:
        root.destroy()
    except:
        pass

    if usertext == False or usertext.strip() == '':
        usertext = False
    
    return {'text':usertext,'xi':usexi}

if __name__ == "__main__":
    print inputbox("receiver","account",True)
