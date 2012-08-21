# -*- coding: utf-8 -*-

import shelve,os,sys,time
import daemon

def get_status(server,user,bits):
    cachepath = os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])),'configs','online.db')
    nowtime = time.time()
    
    sh = shelve.open(cachepath,writeback=True)
    if not sh.has_key(server):
        sh[server] = {}
    if not sh[server].has_key(user):
        sh[server][user] = {'lastcheck':0,'lastupdate':0}

    if nowtime - sh[server][user]['lastupdate'] > 60:
        sh[server][user]['lastupdate'] = nowtime

        chk = daemon.query_onlinestate(server,user,bits)
        if chk != False:
            sh[server][user]['lastcheck'] = chk

    chk = sh[server][user]['lastcheck']
    diff = nowtime - chk

    if   diff < 0:
        return -3 # ERR
    elif diff < 60:
        return 1 # Active
    elif diff < 120:
        return 0 # inactive
    elif diff < 300:
        return -1 # gone away
    else:
        return -2 # offline
if __name__ == '__main__':
    print get_status('babeltower.sinaapp.com','lichaobai')
