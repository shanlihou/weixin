#coding=utf8
import threading
from DBHelper import DBHelper
import random
import time
import string
Lock = threading.Lock()
class userHelper(object):
    __instance = None
    mDict = {}
    names = {}
    id = 1
    countDict = {}
    timeDict = {}
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
            name = self.db.dataDecode(i[0])
            self.mDict[name] = i[1]
            
    def getNickList(self, msg):
        nickList =[]
        for i in msg['User']['MemberList']:
            print i
            if i['DisplayName']:
                nickList.append(i['DisplayName'])
            else:
                nickList.append(i['NickName'])
        return nickList
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
    def getID(self, name):
        print name
        if not self.names.has_key(name):
            print self.id
            self.names[name] = self.id
            self.id += 1
        return self.names[name]
    def give(self, name1, name2, score):
        name2 = name2.decode('utf8')
        score1 = self.getScore(name1)
        score2 = self.getScore(name2)
        num = string.atoi(score)
        if num > score1:
            return '所送分数超过你所能给'
        score1 -= num 
        score2 += num
        self.updateScore(name1, score1)
        self.updateScore(name2, score2)
        return 'give成功，give到%d分' % num
        
    def steal(self, name1, name2):
        if self.countDict.has_key(name1):
            if self.countDict[name1] == 5:
                if self.timeDict.has_key(name1):
                    now = time.time()
                    if now - self.timeDict[name1] < 3600:
                        return '冷却中，还有%f秒才能使用' % (3600 + self.timeDict[name1] - now)
                    else:
                        self.countDict[name1] = 0
        else:
            self.countDict[name1] = 0
        self.countDict[name1] += 1
        if self.countDict[name1] == 5:
            self.timeDict[name1] = time.time()
        name2 = name2.decode('utf8')
        score1 = self.getScore(name1)
        score2 = self.getScore(name2)
        if score2 < 20:
            self.countDict[name1] -= 1
            return '操作失败，不能偷取低于20分的人'
        num = random.randint(1, 5)
        if num == 1:
            score1 -= 10
            self.updateScore(name1, score1)
            return '偷取失败， 扣10分'
        num = random.randint(1, 20)
        score1 += num 
        score2 -= num
        self.updateScore(name1, score1)
        self.updateScore(name2, score2)
        return '偷取成功，偷到%d分' % num
        
            
        
