import os
def hashcash(resource,bits=20):
    x = os.popen("hashcash -es -mb %d %s" % (bits,resource))
    h = x.readline()
    return h

if __name__ == '__main__':
    print hashcash('admin')