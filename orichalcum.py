# -*- coding: utf-8 -*-
from Tkinter import *

class Main(object):
    def __init__(self):
        self.root = Tk()
        self._CreateWidgets()
        self.refreshContacts()
    def refreshContacts(self):
        self.userlist.insert(END,'hello')
    def _CreateWidgets(self):
        self.root.title("Orichalcum")
        self.root.resizable(0,0)
        
        self.frame = Frame(self.root)
        self.frame.grid(row=0,column=0)
        
        self.menus = Menu(self.root)
        
        self.mnuMain = Menu(self.menus,tearoff=0)
        self.mnuMain.add_command(label="hello")
        self.mnuMain.add_command(label="world")
        self.menus.add_cascade(label="操作",menu=self.mnuMain)
        
        self.root.config(menu=self.menus)
        
        self.userlist = Listbox(self.frame,width=30,height=30)
        self.userlist.grid(row=1,column=0)
    def Show(self):
        self.root.mainloop()
    
    
if __name__ == '__main__':
    frmMain = Main()
    frmMain.Show()