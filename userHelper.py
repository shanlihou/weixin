import threading
from DBHelper import DBHelper
import string
Lock = threading.Lock()
class userHelper(object):
    __instance = None
    mDict = {}
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(userHelper, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        self.db = DBHelper()
        result = self.db.userQuery()
        for i in result:
            self.mDict[i[0]] = i[1]
            
    def getScore(self, username):
        if self.mDict.has_key(username):
            return self.mDict[username]
        self.mDict[username] = 100
        self.db.userInsert(username, 100)
        return 100
    
    def updateScore(self, username, score):
        if self.mDict.has_key(username):
            self.mDict[username] = score
            self.db.userUpdate(username, score)
        else:
            self.mDict[username] = score
            self.db.userInsert(username, score)
    def sort(self):
        return sorted(self.mDict.items(), key = lambda x: x[1], reverse=True)
        
            
        
