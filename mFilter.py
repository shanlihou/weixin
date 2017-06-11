#coding=utf8
import threading
Lock = threading.Lock()
class mFilter(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(mFilter, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    
    def __init__(self):
        self.db = DBHelper()
        print id(self.db)
        tmpList = self.db.mFiltQuery()
        for i in tmpList:
            self.filtDict[i[1]] = i[2]
    def filter(self, data):
        if self.filtDict.has_key(data):
            return self.filtDict[data]
        return None
    def insert(self, key, value):
        if self.filtDict.has_key(key):
            self.filtDict[key] = value
            self.db.mFiltUpdate(key, value)
        else:
            self.filtDict[key] = value
            self.db.mFiltInsert(key, value)
    def get(self, key):
        if self.filtDict.has_key(key):
            return self.filtDict[key]
        return None
    '''
    def delete(self, key):
        for i in self.filtDict:
            print type(i), i
        print type(key), key
        if self.filtDict.has_key(key.decode('utf8')):
            print 'enter in'
            self.filtDict.pop(key.decode('utf8'))
            self.db.mFiltDelete(key)
            return True
        return False
    '''