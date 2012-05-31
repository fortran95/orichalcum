# -*- coding: utf-8 -*-

from Tkinter import *
import shelve,os,sys,copy,base64,time,tkMessageBox,subprocess,tkFileDialog

BASEPATH = os.path.dirname(sys.argv[0])
if BASEPATH != '':
    BASEPATH += '/'

class message_list(object):
    message_cache = {}
    pointer = 0
    readlist = []
    
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
        
        self.refresh_message()
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.mainloop()
    def quit(self):
        global BASEPATH
        # Will destroy all messages. First, lock up the database.
        while True:
            if os.path.isfile(BASEPATH + 'configs/msgdb.lock'):
                print 'Orichalcum processor: Message database locked, waiting.'
                time.sleep(0.5)
            else:
                dblock = open(BASEPATH + 'configs/msgdb.lock','w+')
                dblock.close()
                break
        # Clear keys.
        db = shelve.open(BASEPATH + 'configs/msgdb.db',writeback=True)
        dellist = []
        for key0 in db:
            for key1 in db[key0]:
                if key1 in self.readlist:
                    dellist.append((key0,key1))
        for t in dellist:
            del db[t[0]][t[1]]
        db.close()
        # Remove lock
        if os.path.isfile(BASEPATH + 'configs/msgdb.lock'):
            os.remove(BASEPATH + 'configs/msgdb.lock')
        # Kill the dialog
        self.root.destroy()
    def refresh_message(self,*args):
        global BASEPATH
        has_message = False
        
        selected = self.userlist_var.get()
        
        db = shelve.open(BASEPATH + 'configs/msgdb.db')
        self.userlist['menu'].delete(0,END)
        self.message_cache = {}
        for key in db:
            if len(db[key]) > 0:
                has_message = True
                keyname = base64.decodestring(key).strip()
                self.message_cache[keyname] = db[key]
                self.userlist['menu'].add_command(label=keyname,command=lambda v=self.userlist_var,l=keyname:v.set(l))
        if not has_message:# Database is empty
            self.root.withdraw()
            tkMessageBox.showwarning("Orichalcum","没有找到新消息，即将退出。")
            exit()
        
        new_display_key = ''
        if self.message_cache.has_key(selected):
            new_display_key = selected
        else:
            new_display_key = keyname
        self.userlist_var.set(new_display_key)
        db.close()
        self.show_user_message()
    def show_user_message(self):
        self.selected = self.userlist_var.get()
        self.protect_pointer()
        if self.message_cache.has_key(self.selected):
            self.poslabel['text'] = '(%d/%d)' % (self.pointer + 1, len(self.message_cache[self.selected]))
            self.set_message(self.message_cache[self.selected].items()[self.pointer][1])     # pass to displaying function.
            
            newreadid = self.message_cache[self.selected].items()[self.pointer][0]
            if not newreadid in self.readlist:
                self.readlist.append(newreadid) # Record the IDs of what we have read.
    def open_reply_window(self):
        global BASEPATH
        self.selected = self.userlist_var.get()
        self.protect_pointer()
        if self.message_cache.has_key(self.selected):
            curmsg = self.message_cache[self.selected].items()[self.pointer][1]
            accname = curmsg['account']
            receiver= self.selected
            #print "command: python send.py -r %s -a %s" % (receiver,accname)
            subprocess.Popen(['python',BASEPATH + 'send.py','-r',receiver,'-a',accname])
    def save_message(self):
        self.selected = self.userlist_var.get()
        self.protect_pointer()
        if self.message_cache.has_key(self.selected):
            curmsg = self.message_cache[self.selected].items()[self.pointer][1]
            accname = curmsg['account']
            receiver= self.selected
            message = curmsg['message']
            msgtime = curmsg['timestamp']
            content = "Orichalcum Message\n\nAccount: %s\nFrom: %s\nTimeStamp: %s\n\n%s" % (accname,receiver,msgtime,message)
            
            myFormats = [('Plain Text Format(*.txt)','*.txt')]
            defname = "%s-%s-%s" % (accname,receiver,msgtime)
            fileName = tkFileDialog.asksaveasfilename(parent=self.root,filetypes=myFormats ,title="Save message", initialfile=defname)
            if len(fileName) > 0:
                #print "Now saving under %s" % fileName
                try:
                    f = open(fileName,'w+')
                    f.write(content)
                    f.close()
                except Exception,e:
                    print e
    def protect_pointer(self):
        if self.pointer < 0:
            self.pointer = 0
        if self.message_cache.has_key(self.selected):
            if self.pointer > len(self.message_cache[self.selected]) - 1:
                self.pointer = len(self.message_cache[self.selected]) - 1
    def pointer_shift(self,offset):
        self.pointer = self.pointer + offset
        self.protect_pointer()
        self.show_user_message()
    def createWidgets(self):
        # Create Labels
        self.label1 = Label(self.root)
        self.label1['text'] = '发件人：'
        self.label1.grid(row=0,column=0)
        # Create Sender Selecting Menu
        self.userlist_var = StringVar(self.root)
        self.userlist_opts= ['----']
        self.userlist_var.set(self.userlist_opts[0])
        self.userlist = OptionMenu(self.root,self.userlist_var,*self.userlist_opts)
        
        self.userlist_var.trace('w',self.refresh_message)
        self.userlist.grid(row=0,column=1,columnspan=2,sticky=N+S+W+E)
        # Create Message Box
        self.message = Text(self.root,width=50,height=20)
        self.message.config(state=DISABLED)
        self.message.grid(row=1,column=0,columnspan=3)
        # Create Navigate Button and Labels
        self.prevbutton = Button(self.root)
        self.prevbutton['text'] = '上一条'
        self.prevbutton['command'] = lambda v=-1: self.pointer_shift(v)
        self.prevbutton.grid(row=2,rowspan=2,column=0,sticky=N+S+W+E)
        
        self.timelabel = Label(self.root)
        self.timelabel['text'] = ''
        self.timelabel['width'] = 23
        self.timelabel.grid(row=2,column=1)
        
        self.poslabel = Label(self.root)
        self.poslabel['text'] = '(0/0)'
        self.poslabel.grid(row=3,column=1)
        
        self.nextbutton = Button(self.root)
        self.nextbutton['text'] = '下一条'
        self.nextbutton['command'] = lambda v=1: self.pointer_shift(v)
        self.nextbutton.grid(row=2,rowspan=2,column=2,sticky=N+S+W+E)
        # Create Save Button
        self.savebutton = Button(self.root)
        self.savebutton['text'] = '保存消息'
        self.savebutton['fg'],self.savebutton['bg'] = ('White','Blue')
        self.savebutton['command'] = self.save_message
        self.savebutton.grid(row=4,column=0,sticky=N+S+W+E)
        # Create Reply Button
        self.replybutton = Button(self.root)
        self.replybutton['text'] = '回复'
        self.replybutton['bg'] = '#0A0'
        self.replybutton['fg'] = 'White'
        self.replybutton['command'] = self.open_reply_window
        self.replybutton.grid(row=4,column=1,columnspan=2,sticky=N+S+W+E)
        # Create Emergency Exit button
        self.exitbutton = Button(self.root)
        self.exitbutton['text'] = '关闭窗口（销毁已读信息）'
        self.exitbutton['bg'] = 'Red'
        self.exitbutton['fg'] = 'White'
        self.exitbutton['command'] = self.quit
        self.exitbutton.grid(row=5,column=0,columnspan=3,sticky=N+S+W+E)
        
        # Update the window.
        self.root.update_idletasks()
    def set_message(self,message):
        self.message.config(state=NORMAL)
        self.message.delete(1.0,END)
        self.message.insert(END,message['message'])
        self.message.config(state=DISABLED)
        timestamp = int(message['timestamp']) - time.timezone
        timetuple = time.gmtime(timestamp)
        self.timelabel['text'] = time.strftime('%Y-%m-%d %H:%M:%S GMT',timetuple)
        
    def select_user(self,event):
        self.userlist.post(event.x_root,event.y_root)
    
frmMessage = message_list()