# -*- coding: utf-8 -*-
import notifier,shelve,base64,sys,os,time,hashlib

BASEPATH = os.path.dirname(sys.argv[0])
if BASEPATH != '':
    BASEPATH += '/'

def handle(message):
    global BASEPATH
    try:
        print message['message']
        # Store message
        #notifier.showMessage(message['sender'],message['message'])
        while True:
            if os.path.isfile(BASEPATH + 'configs/msgdb.lock'):
                print 'Orichalcum processor: Message database locked, waiting.'
                time.sleep(0.5)
            else:
                dblock = open(BASEPATH + 'configs/msgdb.lock','w+')
                dblock.close()
                break
        
        db = shelve.open(BASEPATH + 'configs/msgdb.db',writeback=True)
        newpiece = {'message':message['message'],'timestamp':message['timestamp']}
        newhash = base64.encodestring(hashlib.md5(message['message'] + message['timestamp']).digest()).strip()
        newkey = base64.encodestring(message['sender'])
        if db.has_key(newkey) == False:
            db[newkey] = {newhash:newpiece}
        else:
            db[newkey][newhash] = newpiece
        db.close()
    except Exception,e:
        print "Error saving message: %s" % e
    # Remove database lock
    if os.path.isfile(BASEPATH + 'configs/msgdb.lock'):
        os.remove(BASEPATH + 'configs/msgdb.lock')
    return True

def notify():
    global BASEPATH
    count = 0
    db = shelve.open(BASEPATH + 'configs/msgdb.db')
    for key in db:
        count += len(db[key])
    if count>0:
        notifier.osd("您有 %d 条新消息" % count)