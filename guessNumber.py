#coding=utf8
import threading
import random
import string
import time
from word import WORD
from userHelper import userHelper
Lock = threading.Lock()

class guessNumber(object):
    __instance = None
    state = 0
    number = 0
    count = 0
    sign = {}
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(guessNumber, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        self.users = userHelper()
        self.word = WORD()
    def parse(self, recv, name, msg):
        score = self.users.getScore(name)
        if recv == '积分':
            return '你的积分为:%s' % (score)
        elif recv == '排行榜':
            nickList = self.users.getNickList(msg)
            strRet = ''
            dictRet = self.users.sort()
            count = 0
            for i in dictRet:
                if i[0] not in nickList:
                    continue
                count += 1
                strRet += str(count) + ':' + i[0] + ':' + str(i[1]) + '\n'
            return strRet
        elif recv == '猜单词':
            return self.word.getRandWord()
        elif recv == '签到':
            timeStr = time.strftime('%m%d')
            signStr = name + timeStr
            if self.sign.has_key(signStr):
                return '签到失败'
            else:
                self.sign[signStr] = 1
                num = random.randint(0, 50)
                score += 100 + num
                self.users.updateScore(name, score)                
                return '签到成功,加 %d 分,当前分数:%s' % (num + 100, str(score))
            
        if recv == '猜数字' and self.state == 0:
            self.state = 1
            self.number = random.randint(0, 999)
            self.count = 10
            return '猜数字开始ʼ'
        elif self.state == 1:
            if recv == '关闭':
                self.state = 0
                return '猜数字结束'
            elif recv.isdigit():
                if score < 10:
                    return '你的积分不足10'
                numTmp = string.atoi(recv)
                strRet = ''
                if numTmp == self.number:
                    score += self.count
                    strRet = '回答正确，获得%s分' % self.count
                    self.state = 0
                    self.number = 0
                    self.count = 0
                elif numTmp > self.number:
                    self.count += 10
                    score -= 10
                    strRet = '大了，扣10分'
                else:
                    self.count += 10
                    score -= 10
                    strRet = '小了，扣10分'
                self.users.updateScore(name, score)
                return strRet
                    
            
