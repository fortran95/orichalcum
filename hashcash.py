import os

def hashcash(sender,resource,bits=20):
    print ":NEW HASHCASH GENERATING:"
    x = os.popen("hashcash -es -mb %s %s:%s" % (bits,sender,resource))
    h = x.readline()
    print "- HASHCASH GENERATED -"
    return h

if __name__ == '__main__':
    print hashcash('admin')