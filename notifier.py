# -*- coding: utf-8 -*-
from Tkinter import *
import pynotify
import time,subprocess,os,sys

BASEPATH = os.path.dirname(sys.argv[0])
if BASEPATH != '':
    BASEPATH += '/'

def osd(message,desc=None):
    global BASEPATH
    ns = subprocess.Popen(['mpg123','-q',BASEPATH + 'alarms/notify.mp3'])
    for i in range(0,3):
        osd_write(message,450.0)
    if desc != None:
        ns = subprocess.Popen(['mpg123','-q',BASEPATH + 'alarms/notify.mp3'])
        for key in desc:
            osd_write(key,1500.0)
    
def osd_write(message,timed=450.0):
    ps = subprocess.Popen('gnome-osd-client -fs',shell=True,stdin=subprocess.PIPE)
    ps.stdin.write("""<message id='test' hide_timeout='%d' osd_vposition='top' osd_halignment='center'>\n\n<span foreground='#FF0000'>%s</span></message>""" % (timed,message))
    ps.communicate()
    time.sleep((timed + 150) / 1000)
def gnotify(message,desc,callback):
    global BASEPATH
    ns = subprocess.Popen(['mpg123','-q',BASEPATH + 'alarms/caution.mp3'])
    pynotify.init("Orichalcum")
    n = pynotify.Notification(message,desc)
    n.set_urgency(pynotify.URGENCY_NORMAL)
    #if callback != None:
        #n.add_action("clicked","Button text", callback, None)
    n.set_timeout(15)
    n.show()
    time.sleep(1)
def showMessage(sender,message):
    root = Tk()
    
    txt = Text(root,width=40,height=10)
    txt.insert(END,message)
    txt.grid(row=0,column=0)
    
    root.title("来自 %s 的消息" % sender)
    root.mainloop()
    
if __name__ == '__main__':
    #osd('未读消息：3条')
    #osd('地震速报',['2008年5月12日 午后2时28分','四川省汶川县发生7.8级地震'])
    def callback():
        print "Clicked!"
    gnotify("New message","content",callback)
    showMessage('a','b')