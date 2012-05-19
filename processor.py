# -*- coding: utf-8 -*-
import notifier
def handle(message):
    try:
        notifier.gnotify('来自 %s 的新消息' % message['sender'],message['message'])
        notifier.showMessage(message['sender'],message['message'])
    except:
        pass
    return True # if successfully handled this message.
