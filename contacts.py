import threading
import itchat
from itchat.content import *
Lock = threading.Lock()
class contacts(object):
    __instance = None
    mList = []
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(contacts, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        pass
    def getDict(self):
        try:  
            groups = itchat.get_chatrooms()
            for i in groups:
                self.mList.append(i[u'UserName'])
        except KeyError:
            print 'keyError'
    def notifyAll(self, strSend):
        if not self.mList:
            self.getDict()
        for i in self.mList:
            itchat.send(u'%s' % (strSend), i)            
    def push(self, wx_id, userName):
        if not self.mDict.has_key(wx_id):
            self.mDict[wx_id] = userName
    def getUserName(self, wx_id):
        if not self.mDict:
            self.getDict()
        return self.mDict[wx_id]
