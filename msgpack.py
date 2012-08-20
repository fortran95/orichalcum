import json,zlib
def enpack(tag,message,usexi):
    return json.dumps({'t':tag,'m':zlib.compress(message,9).encode('base64').replace('\n',''),'x':usexi})

def depack(s):
    x = json.loads(s)
    return {'tag':x['t'],
            'message':zlib.decompress(x['m'].decode('base64')),
            'xi':x['x']}
