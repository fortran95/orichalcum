# -*- coding: utf-8 -*-

# This is used to check and pull messages from given server.

import ConfigParser, os, pycurl, StringIO, urllib, json, shelve
import hashcash

def check_messages_list(server,username,secret):
    hc = hashcash.hashcash(username)
    
    html = StringIO.StringIO()
    url = "https://%s/pull.php" % server
    post = {'hashcash':hc,'secret':secret}
    
    c = pycurl.Curl()
    c.setopt(pycurl.URL,url)
    c.setopt(pycurl.SSL_VERIFYHOST, False)
    c.setopt(pycurl.SSL_VERIFYPEER,False)
    c.setopt(pycurl.WRITEFUNCTION, html.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(post))
    c.perform()
    
    if c.getinfo(pycurl.HTTP_CODE)==200:
        retrived = html.getvalue()
        try:
            j = json.loads(retrived)
        except:
            return False
        return j
    else:
        return False
def pull_message(server,messageid):
    hc = hashcash.hashcash(messageid)
    
    html = StringIO.StringIO()
    url = "http://%s/pull.php" % server
    post = {'hashcash':hc,'secret':''}
    
    c = pycurl.Curl()
    c.setopt(pycurl.URL,url)
    c.setopt(pycurl.WRITEFUNCTION, html.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(post))
    c.perform()
    
    if c.getinfo(pycurl.HTTP_CODE)==200:
        retrived = html.getvalue()
        try:
            j = json.loads(retrived)
        except:
            return False
        return j
    else:
        return False
def push_message(server,receiver,message):
    hc = hashcash.hashcash(receiver)
    
    html = StringIO.StringIO()
    url = "http://%s/push.php" % server
    post = {'hashcash':hc,'message':message}
    
    c = pycurl.Curl()
    c.setopt(pycurl.URL,url)
    c.setopt(pycurl.WRITEFUNCTION, html.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(post))
    c.perform()
    
    if c.getinfo(pycurl.HTTP_CODE)==200:
        retrived = html.getvalue()
        return retrived
    else:
        return False
if __name__ == '__main__':
#    host = 'babeltower.sinaapp.com'
#    #print push_message(host,'admin',"""
#    print "geting codes."
#    codes = check_messages_list(host,'admin','admin')
#    if codes != False:
#        print codes
#        print "-- geting first message."
#        j = pull_message('babeltower.sinaapp.com',codes[0])
#        if j != False:
#            print "-- message is here --"
#            print j['message']
#    #""")
    sh = shelve.open("orichalcum.db",writeback=True)
    sh.close()