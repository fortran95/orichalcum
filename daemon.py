# -*- coding: utf-8 -*-

# This is used to check and pull messages from given server.

import ConfigParser, os, pycurl, StringIO, urllib, json, shelve, hashlib, hmac, time
import hashcash
def victoria_decrypt(inputstr,key):
    output = ''
    keylen = len(key)
    dicti = '0123456789abcdef0123456789abcdef'
    inputstr = inputstr.strip().lower()
    key = key.strip().lower()
    i = 0
    while(True):
        pos = dicti.index(inputstr[0:1],16)
        pos -= dicti.index(key[i:i+1])
        output += dicti[pos:pos+1]
        
        inputstr = inputstr[1:]
        i += 1
        if(i >= keylen):
            i = 0
        if inputstr == '':
            break
    return output
def check_messages_list(server,username,secret,bits=22):
    hc = hashcash.hashcash(username,username,bits).strip()
    hc_sha1 = hashlib.sha1(hc).hexdigest().lower()
    auth = hmac.HMAC(secret,hc_sha1,hashlib.sha512).hexdigest().lower()
    
    html = StringIO.StringIO()
    url = "http://%s/pull.php" % server
    post = {'hashcash':hc,'auth':auth}
    
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
            seed = j['seed'].strip()
            deckey = hmac.HMAC(secret,seed,hashlib.sha1).hexdigest()
            codes = []
            for c in j['codes']:
                codes.append(victoria_decrypt(c,deckey))
        except Exception,e:
            print "Error: %s" % retrived
            return False
        return codes
    else:
        return False
def pull_message(server,user,messageid,bits=22):
    hc = hashcash.hashcash(user,messageid,bits)
    
    html = StringIO.StringIO()
    url = "http://%s/pull.php" % server
    post = {'hashcash':hc,'auth':''}
    
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
def push_message(server,sender,secret,receiver,message,bits=22):
    hc = hashcash.hashcash(sender,receiver,bits).strip()
    
    auth = hmac.HMAC(secret,hashlib.sha1(hc).hexdigest().lower(),hashlib.sha512).hexdigest().lower()
    
    html = StringIO.StringIO()
    url = "http://%s/push.php" % server
    post = {'hashcash':hc,'message':message,'auth':auth}
    
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
    host = 'babeltower.sinaapp.com'
    #print push_message(host,'admin','admin','admin',"""
    print "geting codes."
    codes = check_messages_list(host,'admin','admin',bits=24)
    if codes != False:
        print codes
        print "-- getting first message."
        j = pull_message('babeltower.sinaapp.com','admin',codes[0],bits=24)
        if j != False:
            print "-- message is here --"
            print j['message']
    #""",bits=24)
    exit()

    accounts = {}
    
    accountfile = ConfigParser.ConfigParser()
    accountfile.read('configs/accounts.cfg')
    
    for secname in accountfile.sections():
        accounts[secname] = {
                'host':accountfile.get(secname,'host'),
                'user':accountfile.get(secname,'user'),
                'secret':accountfile.get(secname,'secret'),
                'lastls':0,
                'lastpull':30,
            }
    
    def job():
        global accounts
        sh = shelve.open("configs/orichalcum.db",writeback=True)
        
        now = time.time()
        for key in accounts:
            if now - acounts[key]['lastls'] > 30:
                accounts[key]['lastls'] = 30
                # VISIT THE SITE
                codes = check_messages_list(accounts[key]['host'],accounts[key]['user'],accounts[key]['secret'],bits=24)
                if codes != False:
                    for code in codes:
                        # Save required code.
                        sh['accounts'][key]['codes'].append(code)
                else:
                    print codes
        sh.close()
    job()
