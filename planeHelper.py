#coding=utf8
from plane import plane
import string
class planeHelper(object):
    def __init__(self):
        self.players = []
        self.game = None
        self.test = 0
        pass
    def startGame(self):
        self.game = plane(len(self.players))
        ran = self.game.rollRan()
        img = [self.game.createFrame()]
        return img, '游戏开始，玩家列表:\n' + self.getPlayers() + '下一玩家:%s\n下一点数:%d' % (self.players[0], ran)
    def getPlayers(self):
        strRet = ''
        count = 0
        for i in self.players:
            count += 1
            strRet += str(count) + '.' + i + '\n'
        return strRet
    def parse(self, recv, name):
        print 'enter:'
        if recv == '飞行棋':
            print 'enter 1'
            if self.game:
                return None, '游戏已经开始'
            if name in self.players:
                return None, '不要执迷不悟，你已经在游戏中了'
            self.players.append(name)
            if len(self.players) == 4:
                return self.startGame()
            return None, '参与玩家:%s' % self.getPlayers()
        elif recv == '飞行棋开始':
            if name in self.players and self.game == None and len(self.players) >= 2:
                self.game = plane
                return self.startGame()
            return None, '你不是玩家或人数少于2'
        elif recv == '飞行棋结束':
            if name in self.players:
                self.game = None
                self.players = []
                return None, '游戏结束'
            return None, '你不是玩家'
        elif recv.startswith('fly'):
            if name not in self.players:
                return None, '你不是玩家'
            elif not self.game:
                return None, '游戏未开始'
            curUser = self.game.getCurColor()
            if self.players[curUser] != name:
                return None, '急什么，没轮到你'
            opt = recv.split(' ')
            if len(opt) == 1:
                opt.append('1')
            if len(opt) == 2 and opt[1].isdigit():
                num = string.atoi(opt[1])
                if num < 1 or num > 4:
                    return None, '能不能好好走棋'
                img, code = self.game.goChess(num - 1)
                ran = self.game.getRan()
                curUser = self.game.getCurColor()
                self.test += 1
                if len(self.players == 1):
                    if curUser == 1:
                        pass
                print 'test:%d' % self.test
                if code == 0:
                    self.game = None
                    self.players = []
                    return img, '%d:游戏结束，获胜玩家:%s' % (self.test, self.players[curUser])
                if code == 1:
                    return img, '%d:走棋成功\n下一玩家:%s\n下一点数:%d' % (self.test, self.players[curUser], ran)
                elif code == 2:
                    return None, '%d:无期可走，抬走，下一个\n下一玩家:%s\n下一点数:%d' % (self.test, self.players[curUser], ran)
                elif code == 3:
                    return None, '%d:恭喜你获得了起飞机会，请走\n下一玩家:%s\n下一点数:%d' % (self.test, self.players[curUser], ran)
            else:
                return None, '能不能好好走棋'
        return None, None
            