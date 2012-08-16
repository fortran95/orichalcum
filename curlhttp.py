import StringIO,urllib,os

internal = True

try:
    import pycurl
except:
    pass

def http(url,post):
    html = StringIO.StringIO()
    if type(post) == dict:
        post = urllib.urlencode(post)

    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL,url)
        c.setopt(pycurl.SSL_VERIFYHOST, False)
        c.setopt(pycurl.SSL_VERIFYPEER,False)
        c.setopt(pycurl.WRITEFUNCTION, html.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.POSTFIELDS, post)
        c.perform()
    
    except Exception,e:
        print "CURL with internal error: %s" % e
        
        try:
            t = os.popen('curl --data "%s" %s' % (post,url))
            s = t.read()
            return s.strip()
        except:
            return False

    return html.getvalue().strip()
    
