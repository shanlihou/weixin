#coding=utf8
import threading
import urllib2
import random
from DBHelper import DBHelper
Lock = threading.Lock()

class WORD(object):
    __instance = None
    ranAlpha = ''
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(WORD, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        self.db = DBHelper()
        self.filt = []
    def getTrans(self, word):
        url='http://dict.youdao.com/w/eng/' + word
        resp = urllib2.urlopen(url)
        html = resp.read()
        indexTrans = html.find('trans-container')
        if indexTrans != -1:
            start = indexTrans + html[indexTrans:].find('<li>')
            end = indexTrans + html[indexTrans:].find('</li>')
            chinese = html[start + len('<li>'):end]
            print chinese
            return chinese
        return None
    def AInB(self, a, b):
        for i in a:
            if i in b:
                b.replace(i, '', 1)
            else:
                return False
        return True
    def checkWord(self, word):
        if word in self.filt:
            return '哥们你回答过这个单词了，失败扣10分', -10
        if not self.AInB(word, self.ranAlpha):
            return '单词没有包含所有字母，失败扣10分', -10
        chinese = self.getTrans(word)
        if chinese:
            self.filt.append(word)
            score = random.randint(1, 5)
            return ('恭喜你，加%d分\n单词释义:' % score) + chinese, score
        else:
            return '这不是个单词啊，大兄弟，扣10分', -10
    def getRandom(self):
        strRet = ''
        for i in range(4):
            ran = random.randint(0, 25)
            strRet += chr(ord('a') + ran)
        self.ranAlpha = strRet
        return '猜单词开始：请组一个单词需包含以下字母:' + strRet
    def getRandWord(self):
        ran = random.randint(1, 135120)
        result = self.db.getWordByNum(ran)
        newWord = result[0][1]
        print 'word:', newWord
        wordList = list(newWord.encode('utf8'))
        wordList = sorted(wordList)
        self.ranAlpha = ''.join(wordList)
        self.filt = []
        return '猜单词开始：请组一个单词需包含以下字母:' + self.ranAlpha