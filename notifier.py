# -*- coding: utf-8 -*-
import pynotify
import time,os,subprocess

def osd(message,desc=None):
    for i in range(0,3):
        osd_write(message)
    if desc != None:
        for key in desc:
            osd_write(key)
def osd_write(message):
    ps = subprocess.Popen('gnome-osd-client -fs',shell=True,stdin=subprocess.PIPE)
    ps.stdin.write("""<message id='test' hide_timeout='450' osd_vposition='top' osd_halignment='center'>\n\n<span foreground='#FF0000'>%s</span></message>""" % message)
    ps.communicate()
    time.sleep(0.6)
def gnotify(message,desc):
    pynotify.init("Orichalcum")
    n = pynotify.Notification(message,desc)
    n.set_urgency(pynotify.URGENCY_NORMAL)
    n.set_timeout(5)
    n.show()
    time.sleep(1)
if __name__ == '__main__':
    osd('未读消息：3条')
    #gnotify('title','my test message')