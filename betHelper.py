#coding=utf8
import threading
from DBHelper import DBHelper
Lock = threading.Lock()
class betHelper(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(betHelper, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        self.db = DBHelper()
        result = self.db.betQuery()
        self.edgeDict = {}
        for i in result:
            self.edgeDict[i[1]] = i[2]
    def setEdge(self, edge, probability):
        if not self.edgeDict.has_key(edge):
            self.edgeDict[edge] = probability
            self.db.betInsert(edge, probability)
        else:
            self.edgeDict[edge] = probability
            self.db.betUpdate(edge, probability)
    def delete(self, edge):
        if not self.edgeDict.has_key(edge):
            return False
        self.edgeDict.pop(edge)
        self.db.betDelete(edge)
        return True
    def printAll(self):
        pass
    def sort(self):
        return sorted(self.edgeDict.items(), key = lambda x: x[0], reverse=True)
            
            
        