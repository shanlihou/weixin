#coding=utf8
import threading
import random
import string
import time
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
    def parse(self, recv, name):
        score = self.users.getScore(name)
        print recv, name
        if recv == '积分':
            return '你的积分为:%s' % (score)
        elif recv == '签到':
            now = time.localtime(time.time())
            timeStr = time.strftime('%m%d')
            signStr = name + timeStr
            if self.sign.has_key(signStr):
                return '签到失败'
            else:
                self.sign[signStr] = 1
                score += 100
                self.users.updateScore(name, score)                
                return '签到成功,当前分数:%s' % (str(score))
        if recv == '猜数字' and self.state == 0:
            self.state = 1
            self.number = random.randint(0, 999)
            self.count = 0
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
                    
            