#coding=utf8
from DBHelper import DBHelper
import threading
Lock = threading.Lock()
class filtHelper(object):
    db = None
    filtDict = {}
    __instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(filtHelper, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    
    def __init__(self):
        self.db = DBHelper()
        print id(self.db)
        tmpList = self.db.filtQuery()
        for i in tmpList:
            self.filtDict[i[0]] = i[1]
    def filter(self, data):
        for key in self.filtDict:
            if key in data:
                return self.filtDict[key]
        return None
    def insert(self, key, value):
        if self.filtDict.has_key(key):
            self.filtDict[key] = value
            self.db.filtUpdate(key, value)
        else:
            self.filtDict[key] = value
            self.db.filtInsert(key, value)
    def get(self, key):
        if self.filtDict.has_key(key):
            return self.filtDict[key]
        return None
    def getX(self, data):
        strRet = ''
        for i in data:
            strRet += str(ord(i)) + ' '
        return strRet
    def delete(self, key):
        '''
        for i in self.filtDict:
            print i, self.getX(i)
        print type(key), key, self.getX(key)
        '''
        if self.filtDict.has_key(key.decode('utf8')):
            print 'enter in'
            self.filtDict.pop(key.decode('utf8'))
            self.db.filtDelete(key)
            return True
        elif self.filtDict.has_key(key):
            print 'enter in'
            self.filtDict.pop(key)
            self.db.filtDelete(key)
            return True
            
        return False

            
    
