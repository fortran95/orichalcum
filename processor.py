# -*- coding: utf-8 -*-
import notifier,shelve,base64,sys,os,time,hashlib,json
import plugins

BASEPATH = os.path.dirname(sys.argv[0])
if BASEPATH != '':
    BASEPATH += '/'
def parse(message):
    # If this is a marked message(with tags. only tag='im' will be shown, others will be transfered to related programs.
    tag=''
    try:
        j = json.loads(message)
        tag = j['tag']
        message = j['message']
    except:
        tag = 'im'
    return {'tag':tag,'message':message}
def handle(message,accountkey):
    global BASEPATH
    try:
        print message['message']
        guidance = parse(message['message'])
        if guidance['tag'] != 'im':
            # Call related programs here !
            plugins.plugin_do(guidance)
            return True
        else:
            message['message'] = guidance['message']
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
        newpiece = {'message':message['message'],'timestamp':message['timestamp'],'account':accountkey}
        newhash = base64.encodestring(hashlib.md5(message['message'] + message['timestamp']).digest()).strip()
        newkey = base64.encodestring(message['sender'])
        if db.has_key(newkey) == False:
            db[newkey] = {newhash:newpiece}
        else:
            db[newkey][newhash] = newpiece
        db.close()
        notifier.gnotify('来自 %s 的消息' % message['sender'], message['message'])
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
