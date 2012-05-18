import os
def hashcash(sender,resource,bits=20):
    x = os.popen("hashcash -es -mb %d %s:%s" % (bits,sender,resource))
    h = x.readline()
    return h

if __name__ == '__main__':
    print hashcash('admin')