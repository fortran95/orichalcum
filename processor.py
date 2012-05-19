# -*- coding: utf-8 -*-
import notifier
def handle(message):
    notifier.gnotify('新消息',message['message'])
    return True # if successfully handled this message.
