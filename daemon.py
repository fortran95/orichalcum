# -*- coding: utf-8 -*-

# This is used to check and pull messages from given server.

import ConfigParser, os, pycurl, StringIO, urllib, json, shelve, hashlib, hmac, time
import hashcash,notifier,processor
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
    
    accounts = {}
    
    accountfile = ConfigParser.ConfigParser()
    accountfile.read('configs/accounts.cfg')
    
    for secname in accountfile.sections():
        accounts[secname] = {
                'host':accountfile.get(secname,'host'),
                'user':accountfile.get(secname,'user'),
                'secret':accountfile.get(secname,'secret'),
                'bits':accountfile.get(secname,'bits'),
                'lastls':0,
                'lastpull':30,
            }
        
    last_message_notify = 0
    
    def job():
        global accounts,last_message_notify
        sh = shelve.open("configs/orichalcum.db",writeback=True)
        
        now = time.time()
        new_messages = 0
        
        if sh.has_key('accounts') == False:
            sh['accounts'] = {}
        
        for key in accounts:
            if now - accounts[key]['lastls'] > 30:
                accounts[key]['lastls'] = now
                # VISIT THE SITE
                codes = check_messages_list(accounts[key]['host'],accounts[key]['user'],accounts[key]['secret'],accounts[key]['bits'])
                if codes != False:
                    print "Listing: %d new message(s) found." % len(codes)
                    for code in codes:
                        # Save required code.
                        if sh['accounts'].has_key(key) == False:
                            sh['accounts'][key] = {'codes':[],'messages':[]}
                        sh['accounts'][key]['codes'].append(code)
                else:
                    print codes
        # Pull messages
        for key in accounts:
            if now - accounts[key]['lastpull'] > 30:
                accounts[key]['lastpull'] = now
                
                pulled = []
                
                if sh['accounts'].has_key(key) == False:
                    sh['accounts'][key] = {'codes':[],'messages':[]}
                
                for pullcode in sh['accounts'][key]['codes']:
                    print "Pulling message ID = %s ..." % pullcode
                    pm = pull_message(accounts[key]['host'],accounts[key]['user'],pullcode,accounts[key]['bits'])
                    if pm != False:
                        print "(Message retrived successfully.)"
                        sh['accounts'][key]['messages'].append(pm)
                    else:
                        print "(Error in retriving message.)"
                    pulled.append(pullcode)
                
                for todel in pulled:
                    if todel in sh['accounts'][key]['codes']:
                        sh['accounts'][key]['codes'].remove(todel)
                        
                dellist = []
                for msgkey in sh['accounts'][key]['messages']:
                    if processor.handle(msgkey) == True:
                        dellist.append(msgkey)
                for todel in dellist:
                    sh['accounts'][key]['messages'].remove(todel)
                    
                    
                new_messages += len(sh['accounts'][key]['messages'])
                
        notify_timed = now - last_message_notify
        if notify_timed > 60:
            if new_messages > 0:
                notifier.osd("%d 条新信息" % new_messages)
                last_message_notify = now
                
            
        sh.close()
# Start daemon.
    while True:
        print ' ' * 10 + "Time to check my job."
        job()
        print ' ' * 10 + "My job finished."
        time.sleep(10)