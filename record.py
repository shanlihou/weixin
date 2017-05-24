#coding=utf8
import threading
Lock = threading.Lock()
class record(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(record, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        self.record = []
        self.nameInfo = {}
        self.count = 0
        self.max = 100
        pass
    def insert(self, name, data, lenth):
        record = None
        info = None
        if self.nameInfo.has_key(name):
            info = self.nameInfo[name]
            record = self.record[info[0]]
        else:
            record = [None] * (self.max + 1)
            record[self.max] = 0
            info = []
            self.record.append(record)
            info.append(self.count)
            self.count += 1
            info.append(lenth)
            self.nameInfo[name] = info
        head = record[self.max]
        record[head] = data
        record[self.max] = (head + 1) % self.max
    def printInfo(self):
        strRet = ''
        for i in self.nameInfo:
            info = self.nameInfo[i]
            strRet += str(info[0]) + ':' + str(info[1]) + '\n'
        return strRet
    def getData(self, index):
        strRet = ''
        record = self.record[index]
        head = record[self.max]
        for i in range(self.max):
            data = record[(head + i) % self.max]
            if data:
                strRet += data + '\n'
        return strRet
            
            
            
            