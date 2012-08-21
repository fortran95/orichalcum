# -*- coding: utf-8 -*-

import shelve,os,sys,time

def get_status(server,user):
    try:
        cachepath = os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])),'configs','online.db')
        nowtime = time.time()
    
        sh = shelve.open(cachepath,writeback=True)
        if not sh.has_key(server):
            sh[server] = {}
        if not sh[server].has_key(user):
            sh[server][user] = {'lastcheck':0,'lastupdate':0,'wantupdate':True}

        if nowtime - sh[server][user]['lastupdate'] > 60:
            sh[server][user]['wantupdate'] = True

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
    except:
        return -3
if __name__ == '__main__':
    print get_status('babeltower.sinaapp.com','lichaobai')
