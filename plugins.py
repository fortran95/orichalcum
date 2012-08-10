handlers = {}

try:
    import akasha
    handlers['akasha'] = akasha.handler
except:
    print "Warning: Akasha cannot be loaded."

def plugin_do(message):
    global handlers
    tag = message['tag']

    if handlers.has_key(tag):
        handlers[tag](message)
        return True
    else:
        return False
