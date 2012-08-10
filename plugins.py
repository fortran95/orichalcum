"""
{'message': u'a2\n', 'tag': u'akasha', 'more': {u'timestamp': u'1344568248', u'account': u'admin', 'sender': 'li.....ai'}}
"""

handlers = {}

try:
    import akasha
    handlers['akasha'] = (akasha.handler,{'keep-record':False})
except:
    print "Warning: Akasha cannot be loaded."

def plugin_do(message):
    global handlers
    tag = message['tag']

    if handlers.has_key(tag):
        handlers[tag][0](message,handlers[tag][1])
        return True
    else:
        return False
