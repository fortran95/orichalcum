#-*- coding: utf-8 -*-

import os,sys,hashlib

VIA = 'orichalcum'
BASEPATH = os.path.realpath(os.path.dirname(sys.argv[0]))
BOXPATH  = os.path.join(BASEPATH,'postoffice','boxes')

XI_ENABLED = os.path.isdir(BOXPATH)

from letter import letter

def xi_process_outgoing():
    global BASEPATH
    os.popen('python ' + os.path.join(BASEPATH,'postoffice','outbox.py'))
def xi_process_incoming():
    global BASEPATH
    os.popen('python ' + os.path.join(BASEPATH,'postoffice','inbox.py'))

def xi_queue(sender,receiver,tag,message,outgoing=True):
    global BOXPATH,VIA

    if outgoing:
        midpath = 'outgoing'
    else:
        midpath = 'incoming'
    
    content = 'SENDER %s\nRECEIVER %s\nVIA %s\nTAG %s\n\n%s' % (sender,receiver,VIA,tag,message)

    filename = os.path.join(BOXPATH,midpath,'queue',hashlib.md5(content).hexdigest())

    open(filename,'w+').write(content)

    if outgoing:
        xi_process_outgoing()
    else:
        xi_process_incoming()

def xi_handled(outgoing = True):
    global BOXPATH,VIA
    ret = []

    if outgoing:
        midpath = 'outgoing'
    else:
        midpath = 'incoming'

    handledpath = os.path.join(BOXPATH,midpath,'handled')
    files = os.listdir(handledpath)

    for filename in files:
        if not filename.startswith(VIA + '.'):
            continue
        fullpath = os.path.join(handledpath,filename)
        if os.path.isfile(fullpath):
            # read file
            try:
                l = letter()
                l.read(fullpath)
                if l.attributes['VIA'] != VIA:
                    continue
                ret.append((l.attributes['SENDER'],l.attributes['RECEIVER'],l.attributes['TAG'],l.body))
            except:
                continue
            os.remove(fullpath)
    return ret

if __name__ == '__main__':
    print XI_ENABLED
