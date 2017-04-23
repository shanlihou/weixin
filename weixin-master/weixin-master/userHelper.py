import threading
from DBHelper import DBHelper
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
        return 0
    
    def updateScore(self, username, score):
        if self.mDict.has_key(username):
            self.mDict[username] = score
        else:
            self.mDict[username] = score
            self.db.userInsert(username, score)
    def addUser(self, username):
        
            
        