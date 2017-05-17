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
        self.chipList = []
        self.chipMoney = 0
        self.sum = 0
        self.ran = -1
        result = self.db.userQuery()
        for i in result:
            name = self.db.dataDecode(i[0])
            self.mDict[name] = i[1]
    def chipIn(self, name, money = 0):
        score = self.getScore(name)
        if name in self.chipList:
            return '得了吧，你已经下注'
        if self.chipMoney == 0:
            if money == 0:
                return '没钱就别下注'
            self.chipMoney = money
            self.chipList.append(name)
            self.sum = money
            score -= money
        else:
            if score < self.chipMoney:
                return '没有钱就别跟注'
            self.sum += self.chipMoney
            self.chipList.append(name)
            score -= self.chipMoney
        self.updateScore(name, score)
        return '下注成功，当前积分:%d' % score
    def setRan(self, ran):
        if ran < len(self.chipList):
            self.ran = ran
            return '操作成功'
        return '操作失败,没这么多人'
    def open(self):
        if len(self.chipList) == 0:
            return '没有人参与，无法开奖'
        ran = 0
        if self.ran == -1:
            ran = random.randint(0, len(self.chipList) - 1)
        else:
            ran = self.ran
        name = self.chipList[ran]
        score = self.getScore(name)
        score += self.sum
        self.updateScore(name, score)
        self.chipList = []
        self.ran = -1
        self.chipMoney = 0
        return '获胜者是:%s，获得%d分,当前积分:%d' % (name, self.sum, score)
    def getChipList(self):
        strRet = ''
        count = 0
        for i in self.chipList:
            count += 1
            strRet += str(count) + ':' + i + '\n'
        return strRet
    def getNickList(self, msg):
        nickList =[]
        username = msg['ActualUserName']
        nickName = ''
        for i in msg['User']['MemberList']:
            if i['UserName'] == username:
                nickName = i['NickName']
            nickList.append(i['NickName'])
        return nickList, nickName
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
            son = self.getScore(u'鱼塘助手')
            son += 10      
            self.updateScore(u'鱼塘助手', son)  
            return '偷取失败， 扣10分'
        num = random.randint(1, 20)
        score1 += num 
        score2 -= num
        self.updateScore(name1, score1)
        self.updateScore(name2, score2)
        return '偷取成功，偷到%d分' % num
        
            
        
