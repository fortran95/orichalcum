# -*- coding: utf-8 -*-
import pynotify
import time,subprocess

def osd(message,desc=None):
    ns = subprocess.Popen(['mpg123','-q','alarms/notify.mp3'])
    for i in range(0,3):
        osd_write(message,450.0)
    if desc != None:
        ns = subprocess.Popen(['mpg123','-q','alarms/notify.mp3'])
        for key in desc:
            osd_write(key,1500.0)
    
def osd_write(message,timed=450.0):
    ps = subprocess.Popen('gnome-osd-client -fs',shell=True,stdin=subprocess.PIPE)
    ps.stdin.write("""<message id='test' hide_timeout='%d' osd_vposition='top' osd_halignment='center'>\n\n<span foreground='#FF0000'>%s</span></message>""" % (timed,message))
    ps.communicate()
    time.sleep((timed + 150) / 1000)
def gnotify(message,desc):
    pynotify.init("Orichalcum")
    n = pynotify.Notification(message,desc)
    n.set_urgency(pynotify.URGENCY_NORMAL)
    n.set_timeout(5)
    n.show()
    time.sleep(1)
if __name__ == '__main__':
    osd('未读消息：3条')
    #osd('地震速报',['2008年5月12日 午后2时28分','四川省汶川县发生7.8级地震'])