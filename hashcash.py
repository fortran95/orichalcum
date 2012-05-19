# This is a modified hashcash generator that used in our Orichalcum and
#  Babeltower system. The generator will first check if your system have
#  hashcash's C generator installed, or use an alternative of Python which
#  will be much slower.

import sys,os,hashlib
from string import ascii_letters
from math import ceil, floor
from random import choice
from time import *

ERR = sys.stderr            # Destination for error messages
DAYS = 60 * 60 * 24         # Seconds in a day
tries = [0]                 # Count hashes performed for benchmark

def hashcash(sender,resource,bits=20):
    print ":NEW HASHCASH GENERATING:"
    usePython = False
    resource = "%s:%s" % (sender,resource)
    try:
        x = os.popen("hashcash -es -mb %s %s" % (bits,resource))
    except:
        usePython = True
    h = x.readline().strip()
    if h == '':
        usePython = True
    if usePython:
        print "WARNING: You currently hasn't a C compiled hashcash generator. This will lose much time."
        h = mint(resource,bits,'',8,True)
    print "- HASHCASH GENERATED -"
    return h

def mint(resource, bits=20, ext='', saltchars=8, stamp_seconds=False):
    """Mint a new hashcash stamp for 'resource' with 'bits' of collision

    20 bits of collision is the default.

    'ext' lets you add your own extensions to a minted stamp.  Specify an
    extension as a string of form 'name1=2,3;name2;name3=var1=2,2,val'
    FWIW, urllib.urlencode(dct).replace('&',';') comes close to the
    hashcash extension format.

    'saltchars' specifies the length of the salt used; this version defaults
    8 chars, rather than the C version's 16 chars.  This still provides about
    17 million salts per resource, per timestamp, before birthday paradox
    collisions occur.  Really paranoid users can use a larger salt though.

    'stamp_seconds' lets you add the option time elements to the datestamp.
    If you want more than just day, you get all the way down to seconds,
    even though the spec also allows hours/minutes without seconds.
    """
    ver = "1"
    ts = strftime("%y%m%d%H%M%S", localtime(time() + timezone))
    
    challenge = "%s:"*6 % (ver, bits, ts, resource, ext, _salt(saltchars))
    return challenge + _mint(challenge, bits)

def _salt(l):
    "Return a random string of length 'l'"
    alphabet = ascii_letters + "+/="
    return ''.join([choice(alphabet) for _ in [None]*l])

def _mint(challenge, bits):
    """Answer a 'generalized hashcash' challenge'

    Hashcash requires stamps of form 'ver:bits:date:res:ext:rand:counter'
    This internal function accepts a generalized prefix 'challenge',
    and returns only a suffix that produces the requested SHA leading zeros.

    NOTE: Number of requested bits is rounded up to the nearest multiple of 4
    """
    counter = 0
    hex_digits = int(ceil(int(bits)/4.))
    zeros = '0'*hex_digits
    while 1:
        digest = hashlib.sha1(challenge+hex(counter)[2:]).hexdigest()
        if digest[:hex_digits] == zeros:
            tries[0] = counter
            return hex(counter)[2:]
        counter += 1

if __name__ == '__main__':
    print hashcash('admin','lichaobai',20)