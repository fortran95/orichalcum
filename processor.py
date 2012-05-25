# -*- coding: utf-8 -*-
import notifier,shelve,base64,sys,os

BASEPATH = os.path.dirname(sys.argv[0])
if BASEPATH != '':
    BASEPATH += '/'

def handle(message):
    global BASEPATH
    try:
        print message['message']
        # Store message
        #notifier.showMessage(message['sender'],message['message'])
        db = shelve.open(BASEPATH + 'configs/msgdb.db',writeback=True)
        newpiece = {'message':message['message'],'timestamp':message['timestamp']}
        newkey = base64.encodestring(message['sender'])
        if db.has_key(newkey) == False:
            db[newkey] = [newpiece]
        else:
            db[newkey].append(newpiece)
        db.close()
    except Exception,e:
        print "Error saving message: %s" % e
    return True

def notify():
    global BASEPATH
    count = 0
    db = shelve.open(BASEPATH + 'configs/msgdb.db')
    for key in db:
        count += len(db[key])
    if count>0:
        notifier.osd("您有 %d 条新消息" % count)