import threading
import random
import string
from userHelper import userHelper
Lock = threading.Lock()

class guessNumber(object):
    __instance = None
    state = 0
    number = 0
    count = 0
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
        if recv == '²ÂÊý×Ö' and self.state == 0:
            self.state = 1
            self.number = random.randint(0, 999)
            self.count = 0
        elif self.state == 1:
            score = self.users.getScore(name)
            if score < 10:
                return
            if recv == '¹Ø±Õ':
                self.state = 0
            elif recv.isdigit():
                numTmp = string.atoi(recv)
                if numTmp == self.number:
                    score += self.count
                    self.users.updateScore(name, score)
                    self.state = 0
                    self.number = 0
                    self.count = 0
                    pass
                elif numTmp > self.number:
                    self.count += 10
                    score -= 10
                    self.users.updateScore(name, score)
                else:
                    self.count += 10
                    score -= 10
                    self.users.updateScore(name, score)
                    
            