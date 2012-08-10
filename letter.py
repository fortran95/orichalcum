# -*- coding: utf-8 -*-

# 提供一个类，用于解析或产生与上层应用交换的信息

class letter(object):
    
    attributes = {}
    items = ('SENDER','VIA','TAG','RECEIVER','ATTRIBUTES')
    body = ''

    def __init__(self):
        pass
    def _validate_value(self,text):
        validchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@.:;-+='
        for c in text:
            if not c in validchars:
                return False
        return True
    def read(self,filename):
        try:
            
            # 接收者和应用名称（这将决定证书信息，但本类不管）
            # 应用标识（不管）
            # 发送者（和应用名称）
            
            f = open(filename,'r').readlines()

            separator = f.index('\n')

            headers = f[0:separator]
            body  = "".join(f[separator+1:]).strip()

            self.attributes = {}
            for l in headers:
                l = l.strip()
                prefix = l[0:l.index(' ')].strip().upper()
                if prefix in self.items:
                    value  = l[l.index(' ') + 1:].strip()
                    if not self._validate_value(value):
                        raise Exception("Invalid attribute value of this letter.")
                    self.attributes[prefix] = value

            # 读取 ATTRIBUTES 给出的消息编码设置，解读消息
            if self.attributes.has_key('ATTRIBUTES'):
                attrs = self.attributes['ATTRIBUTES'].lower().split(';')
                if 'base64' in attrs:
                    body = body.decode('base64')
            
            self.body = body

        except Exception,e:
            print e
            raise Exception("Unable to read this letter.")
    def write(self,filename):
        try:
            
            body = ''

            # 根据body和attributes的设置，写入文件
            for attr in self.attributes:
                value = self.attributes[attr]
                attr  = attr.upper()
                if attr in self.items:
                    if not self._validate_value(value):
                        raise Exception("Invalid attribute value of this letter.")
                    body += '%16s %s\n' % (attr,value)
            body += '\n'
            
            # 根据attributes做出处理
            t = self.body[:]
            if self.attributes.has_key('ATTRIBUTES'):
                attrs = self.attributes['ATTRIBUTES'].lower().split(';')
                if 'base64' in attrs:
                    t = t.encode('base64')
            
            body += t

            open(filename,'w+').write(body)                    

        except Exception,e:
            print e
            raise Exception("Failed writing a letter.")

if __name__ == '__main__':
    l = letter()
    l.attributes = {'receiver':'orxszlyzr','sender':'rijndael','via':'babeltower','tag':'tag'}
    l.body = 'Hello, world!'
    l.write('outbox/sample')
