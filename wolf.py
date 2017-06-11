#coding=utf8
import threading
from DBHelper import DBHelper
import datetime
import time
Lock = threading.Lock()
class wolf(object):
    __instance = None
    mDict = {}
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(wolf, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        self.db = DBHelper()
        result = self.db.wolfQuery()
        for i in result:
            name = self.db.dataDecode(i[1])
            self.mDict[name] = i[2]
    def getCurWeek(self):   
        d = datetime.datetime.now() 
        sun = 6 - d.weekday()
        now = time.localtime(time.time() + sun * 24 * 3600)
        strRet = '%d%02d%02d' % (now.tm_year, now.tm_mon, now.tm_mday)
        return strRet
    def sign(self, name):
        tmpTime = self.getCurWeek()
        if self.mDict.has_key(name):
            self.db.wolfUpdate(name, tmpTime)
        else:
            self.db.wolfInsert(name, tmpTime)
        self.mDict[name] = tmpTime
        return self.getAll()
    def getAll(self):
        tmpTime = self.getCurWeek()
        strRet = '本周游戏车队发车啦:\n呜呜呜呜呜呜呜~~\n'
        count = 0
        for i in self.mDict.items():
            if i[1] == tmpTime:
                count += 1
                strRet += str(count) + '.' + i[0] + '\n'
        return strRet
        
            
        