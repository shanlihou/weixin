#coding=utf8
import urllib2
import urllib
import itchat
from itchat.content import *
import sys  
from magnet import getAllMagnet
import re
import threading
import time 
import os
import json
import random
import string
from wolf import wolf
from zzckz import cicy
from contacts import contacts
from betHelper import betHelper
#from logWeixin import logWeixin
from DBHelper import DBHelper
from filter import filtHelper
from throwGame import throwGame
from gifHelper import gifHelper
import datetime
from guessNumber import guessNumber
from userHelper import userHelper
from word import WORD
import threading
from planeHelper import planeHelper
import math
from record import record
Lock = threading.Lock()
reload(sys)  
sys.setdefaultencoding('utf8')  
DB = DBHelper() 
contact = contacts()
filt = filtHelper()
guess = guessNumber()
users = userHelper()
gWord = WORD()
gif = gifHelper()
brain = None
ran = random.randint(1, 100)
planeGame = planeHelper()
BET = betHelper()
RECORD = record()
WOLF = wolf()
def betRate(x):
    if x < -20000:
        return int(50 - 20 * math.pow(0.9999, -20000 - x))
    else:
        return int(50 + 20 * math.pow(0.9999, x + 20000))
def post(data):
    #data=urllib.quote_plus(data)
    url = 'http://60.205.206.18/?signature=58a37c24b16f9f442d8854f44edaf85d0687183b&timestamp=1480424201&nonce=2011091517&openid=o1zOPuInKqVUN-7ILHP49CVEIIzs'
    data = '<xml><ToUserName><![CDATA[gh_2e3470ff053c]]></ToUserName><FromUserName><![CDATA[123]]></FromUserName><CreateTime>1480427536</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[' + data + ']]></Content><MsgId>6358387851629769718</MsgId></xml>'
    req = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(req)
    return response.read()
infoList = [u'text', u'name', u'detailurl', u'url']
def parseJson(stJson):
    global infoList
    strRet = ''
    if type(stJson) == list:
        for i in stJson:
            strRet += parseJson(i)
    elif type(stJson) == dict:
        for key in stJson:
            if key.encode('utf8') in infoList:
                strRet += stJson[key] + '\n'
            else:
                strRet += parseJson(stJson[key])
    return strRet
def robotChat(data, id):
    print 'id:', id
    url='http://openapi.tuling123.com/openapi/api/v2'
    data = data.encode("utf-8")
    data = '{"perception":{"inputText":{"text":"' + data + '"},"selfInfo":{"location":{"city":"杭州","latitude":"30.26","longitude":"120.19","nearest_poi_name":"大华股份","province":"浙江","street":"滨安路"},}},"userInfo":{"apiKey":"bd7514ba69cf46ab9669c07e3a1ce440","userId":'+ str(id) + '}}'
    req = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(req)
    resp = response.read()
    stJson = json.loads(resp)
    '''
    startStr = '"values":{"text":"'
    start = resp.index(startStr)
    end = resp.index('"}}]}')
    return resp[start + len(startStr):end]'''
    strRet = ''
    strRet = parseJson(stJson)
    return strRet
def authority(name):
    me = itchat.search_friends(remarkName='父母')  
    if me:
        for i in me:
            if name == i['UserName']:
                return True
    return False
            
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print 'text_reply:' 
    print msg
    recv = robotChat(msg['Text'], 1)
    print msg['FromUserName']
    itchat.send('%s: %s' % (msg['Type'], recv), msg['FromUserName'])

# 以下四类的消息的Text键下存放了用于下载消息内容的方法，传入文件地址即可
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print 'download_files:' 
    print msg
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# 收到好友邀请自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    print 'add_friend:' 
    print msg
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])
    userInfo = itchat.search_friends(userName = msg['RecommendInfo']['UserName'])
    wx_id = userInfo[0][u'Uin']
    contact.push(wx_id, msg['RecommendInfo']['UserName'])

# 在注册时增加isGroupChat=True将判定为群聊回复
@itchat.msg_register(TEXT, isGroupChat = True)
def groupchat_reply(msg):
    global DB
    data = msg['Content'].encode("utf-8")
    nickList, nickName = users.getNickList(msg)
    #itchat.get_head_img(userName = msg['ActualUserName'], picDir = '1.gif')
    print nickName, ':', data
    global ran
    wx_id = 0
    RECORD.insert(msg['FromUserName'], nickName + ':' + data, len(msg['User']['MemberList']))
    #print itchat.get_contact(username = msg['ActualUserName'])
    if msg['isAt']:
        recvMsg = msg['Content'].replace('@鱼塘助手', '').replace(' ', '').replace(' ', '')
        recv = robotChat(recvMsg, 100 + users.getID(msg['FromUserName']))
        score = users.getScore(nickName)
        son = users.getScore(u'鱼塘助手')
        if len(recvMsg) == 4 and len(recv) == 5:
            num = random.randint(1, 10)
            score += num
            son -= num      
            recv += ',回答正确，加%d分,当前%d分' % (num, score)
        elif recv.startswith('你接错了，退出成语接龙模式！'):
            score -= 10
            son += 10
            recv += ',扣10分'
        users.updateScore(nickName, score)
        users.updateScore(u'鱼塘助手', son)     
        itchat.send(u'%s' % (recv), msg['FromUserName'])
        return 
    elif data.startswith('movie '):
        print data
        recv = msg['Content']
        mvList = getAllMagnet(recv[len('movie '):])
        strRet = ''
        if mvList:
            for i in mvList:
                strRet += '\n\n' + i
            itchat.send(u'%s' % (strRet), msg['FromUserName'])
            return
        itchat.send(u'%s 搜索失败' % (recv[len('movie ')]), msg['FromUserName'])
        
    elif data.startswith('notify'): 
        if not authority(msg['ActualUserName']):
            itchat.send(u'你不是gm', msg['FromUserName']) 
            return
        notify = data.split(' ')
        if notify[1].isdigit() and len(notify[1]) == 4 and len(notify[2]) < 50:
            if len(notify) == 3:
                DB.insert(notify[1], notify[2])
                itchat.send(u'添加操作成功', msg['FromUserName'])
            elif len(notify) == 4 and notify[3].isdigit():
                DB.insert(notify[1], notify[2], notify[3])   
                itchat.send(u'添加操作成功', msg['FromUserName']) 
    elif data.startswith('shell'): 
        me = itchat.search_friends(remarkName='父母')  
        if me:
            for i in me:
                userName = i['UserName']
                if userName == msg['ActualUserName']:
                    shell = data.split(' ', 1)[1]
                    print shell
                    output = os.popen(shell)
                    itchat.send(u'%s' % (output.read().decode('gbk')), msg['FromUserName']) 
                    return
        itchat.send(u'操作失败', msg['FromUserName']) 
        
    elif data.startswith('week'):
        opt = data.split(' ')
        if len(opt) >= 4 and opt[1].isdigit() and opt[2].isdigit() and len(opt[1]) <= 7 and len(opt[2]) == 4 and len(opt[3]) < 50:
            if len(opt) == 5 and opt[4].isdigit() and len(opt[4]) == 3:
                DB.allInsert(wx_id, opt[1], opt[2], opt[3], opt[4])
                itchat.send(u'添加操作成功', msg['FromUserName'])
            else:
                DB.allInsert(wx_id, opt[1], opt[2], opt[3], '000')
                itchat.send(u'添加操作成功', msg['FromUserName'])
            return
        itchat.send(u'操作失败', msg['FromUserName']) 
    elif data.startswith('day'):
        opt = data.split(' ')
        if len(opt) >= 4 and opt[1].isdigit() and opt[2].isdigit() and len(opt[1]) == 4 and len(opt[2]) == 4 and len(opt[3]) < 50:
            if len(opt) == 5 and opt[4].isdigit() and len(opt[4]) == 3:
                DB.allInsert(wx_id, opt[1], opt[2], opt[3], opt[4])
                itchat.send(u'添加操作成功', msg['FromUserName'])
            else:
                DB.allInsert(wx_id, opt[1], opt[2], opt[3], '010')
                itchat.send(u'添加操作成功', msg['FromUserName'])
            return 
        itchat.send(u'操作失败', msg['FromUserName']) 
    elif data.startswith('filt'):
        opt = data.split(' ')
        if len(opt) == 3 and len(opt[2]) < 50 and len(opt[1]) < 20:
            if opt[1] == 'delete':
                if filt.delete(opt[2]):
                    itchat.send(u'删除成功', msg['FromUserName']) 
                    return 
                else:
                    itchat.send(u'操作失败', msg['FromUserName']) 
                    return
            filt.insert(opt[1], opt[2])
            itchat.send(u'添加操作成功', msg['FromUserName']) 
            return 
        itchat.send(u'操作失败', msg['FromUserName']) 
    elif data.startswith('print'):
        if not authority(msg['ActualUserName']):
            itchat.send(u'你不是gm', msg['FromUserName']) 
            return
        opt = data.split(' ')
        if len(opt) == 2:
            if opt[1] == 'notify' or opt[1] == 'notify_all' or opt[1] == 'filter' or opt[1] == 'user_info' or opt[1] == 'bet':
                strRet = DB.printDB(opt[1])
                itchat.send(u'%s' % (strRet), msg['FromUserName']) 
                return 
        itchat.send(u'操作失败', msg['FromUserName']) 
        return
    elif data.startswith('delete'):
        if not authority(msg['ActualUserName']):
            itchat.send(u'你不是gm', msg['FromUserName']) 
            return
        opt = data.split(' ')
        if len(opt) == 3 and opt[1] == 'bet' and opt[2].isdigit():
            ret = BET.delete(string.atoi(opt[2]))
            if ret:
                itchat.send(u'操作成功', msg['FromUserName']) 
                return
            else:
                itchat.send(u'操作失败', msg['FromUserName']) 
                return
        elif len(opt) == 3 and opt[2].isdigit():
            if opt[1] == 'notify':
                DB.delete(opt[2])
            elif opt[1] == 'notify_all':
                DB.allDelete(opt[2])
            itchat.send(u'操作成功', msg['FromUserName']) 
            return
        itchat.send(u'操作失败', msg['FromUserName']) 
        return
    elif data.startswith('steal'):
        opt = data.split(' ')
        if len(opt) == 2:
            name = opt[1].replace(' ', '')
            if name in nickList:
                recv = users.steal(nickName, name)
                itchat.send(u'%s' % (recv), msg['FromUserName'])
                return
        itchat.send(u'操作失败', msg['FromUserName']) 
        return  
    elif data.startswith('set'):   
        me = itchat.search_friends(remarkName='父母')  
        if me:
            for i in me:
                userName = i['UserName']
                if userName == msg['ActualUserName']:
                    opt = data.split(' ')
                    if len(opt) == 3 and opt[1].isdigit() and opt[2].isdigit():
                        BET.setEdge(string.atoi(opt[1]), string.atoi(opt[2]))
                        itchat.send(u'操作成功', msg['FromUserName']) 
                        return
                    elif len(opt) == 3 and opt[1] == 'prob' and opt[2].isdigit():
                        ran = string.atoi(opt[2])
                        itchat.send(u'操作成功', msg['FromUserName']) 
                        return
                    users.updateScore(opt[1].decode('utf8'), string.atoi(opt[2]))
                    itchat.send(u'操作成功', msg['FromUserName']) 
                    return
        itchat.send(u'操作失败', msg['FromUserName']) 
        return
    elif data.startswith('give'):
        opt = data.split(' ')
        if len(opt) == 3:
            name = opt[1].replace(' ', '')
            print 'enter give'
            if name in nickList:
                print 'enter 1'
                recv = users.give(nickName, name, opt[2])
                itchat.send(u'%s' % (recv), msg['FromUserName'])
                return
        itchat.send(u'操作失败', msg['FromUserName']) 
        return  
    elif data.startswith('word'):
        opt = data.split(' ')
        if len(opt) == 2 and opt[1].isalpha():
            strRet, plus = gWord.checkWord(opt[1]) 
            score = users.getScore(nickName)
            son = users.getScore(u'鱼塘助手')
            score += plus
            son -= plus
            users.updateScore(nickName, score)
            users.updateScore(u'鱼塘助手', son)
            itchat.send(u'%s' % strRet, msg['FromUserName'])
            return 
        itchat.send(u'操作失败', msg['FromUserName']) 
        return
    elif data.startswith('throw'):
        global brain
        if not brain:
            itchat.send(u'游戏未开始', msg['FromUserName']) 
            return     
        opt = data.split(' ')
        if len(opt) == 4 and opt[1].isdigit() and opt[2].isdigit() and opt[3].isdigit():
            angle = string.atoi(opt[1])
            fire = string.atoi(opt[2])
            offset = string.atoi(opt[3])
            if angle > 80 or angle < 0 or fire < 0 or fire > 100 or offset < 0 or offset > 127:
                itchat.send(u'角度1-79， 火力1-100， 位移1-127，而你不符合规范', msg['FromUserName']) 
                return 
            Lock.acquire()
            img, ret = brain.throw(string.atoi(opt[1]), string.atoi(opt[2]), string.atoi(opt[3]))
            gif.createGIF('throw.gif', img, 256, 256, 0, 0)
            itchat.send_image('throw.gif', msg['FromUserName'])
            score = users.getScore(nickName)
            son = users.getScore(u'鱼塘助手')
            print type(ret)
            if ret == 0:
                score += 20
                son -= 20
                brain = None
                itchat.send(u'击中目标，加20分,游戏结束', msg['FromUserName'])
            elif ret == 2:
                score -= 10
                son += 10
                brain = None
                itchat.send(u'次数用尽，扣10分', msg['FromUserName'])                  
            else:
                son += 10
                score -= 10
                itchat.send(u'脱靶，扣10分', msg['FromUserName']) 
            users.updateScore(u'鱼塘助手', son)
            users.updateScore(nickName, score)    
            Lock.release()               
            return
        itchat.send(u'操作失败', msg['FromUserName']) 
        return 
    elif data.startswith('bet'):
        opt = data.split(' ')
        if len(opt) == 2 and opt[1].isdigit():
            score = users.getScore(nickName)
            son = users.getScore(u'鱼塘助手')
            value = string.atoi(opt[1])
            result = BET.sort()
            edge = 50
            for i in result:
                if value > i[0]:
                    edge = i[1]
                    break
            print 'edge:', edge
            if nickName == '蜡笔小丸子' or nickName == '暴走的应工' or nickName == '隔夜果酱':
                ran -= 10
            if value > score:
                itchat.send(u'你就没这多钱，还想下注，做梦呢？', msg['FromUserName'])    
                return
            if ran < edge:
                score += value
                son -= value
                itchat.send(u'恭喜你，压中了，当前积分:%d' % score, msg['FromUserName']) 
            else:
                score -= value   
                son += value
                itchat.send(u'押注失败，当前积分:%d' % score, msg['FromUserName']) 
            ran = random.randint(1, 100)
            users.updateScore(nickName, score)    
            users.updateScore(u'鱼塘助手', son)  
            return
        '''
        elif len(opt) == 3 and opt[2].isdigit():
            value = string.atoi(opt[2])
            name = opt[1].replace(' ', '')
            score = users.getScore(nickName)
            he = users.getScore(name.decode('utf8'))
            if value > score or value > he:
                itchat.send(u'抱歉，你或他没有这么多分？', msg['FromUserName'])    
                return
            if name not in nickList:
                itchat.send(u'此人不存在，你还想跟他对赌', msg['FromUserName'])
                return
            
            if ran < 51:
                score += value
                he -= value
                itchat.send(u'恭喜你，赢了，当前积分:%d' % score, msg['FromUserName']) 
            else:
                score -= value   
                he += value
                itchat.send(u'你输了，当前积分:%d' % score, msg['FromUserName']) 
            ran = random.randint(1, 100)
            users.updateScore(nickName, score)    
            users.updateScore(name.decode('utf8'), he)  
            return
        '''
        itchat.send(u'操作失败', msg['FromUserName']) 
        return 
    elif data.startswith('record'):
        if not authority(msg['ActualUserName']):
            itchat.send(u'你不是gm', msg['FromUserName']) 
            return
        opt = data.split(' ')
        if len(opt) == 2 and opt[1].isdigit():
            index = string.atoi(opt[1])
            strRet = RECORD.getData(index)
            itchat.send(u'%s' % strRet, msg['FromUserName']) 
            return
        elif len(opt) == 2 and opt[1] == 'print':
            strRet = RECORD.printInfo()
            itchat.send(u'%s' % strRet, msg['FromUserName']) 
            return
        itchat.send(u'操作失败', msg['FromUserName']) 
        return
            
    elif data.startswith('chip'):
        opt = data.split(' ')
        if len(opt) == 1:
            opt.append('0')
        if len(opt) == 2 and opt[1].isdigit():
            money = string.atoi(opt[1])
            strRet = users.chipIn(nickName, money)
            itchat.send(u'%s' % strRet, msg['FromUserName']) 
            return
        elif len(opt) == 2 and opt[1].isalpha():
            if opt[1] == 'open':
                strRet = users.open()
                itchat.send(u'%s' % strRet, msg['FromUserName']) 
                return
            elif opt[1] == 'get':
                strRet = users.getChipList()
                itchat.send(u'%s' % strRet, msg['FromUserName']) 
                return
        elif len(opt) == 3 and opt[1].isalpha() and opt[2].isdigit():
            if opt[1] == 'set':
                ran = string.atoi(opt[2])
                strRet = users.setRan(ran)
                itchat.send(u'%s' % strRet, msg['FromUserName']) 
                return
                
        itchat.send(u'操作失败', msg['FromUserName']) 
        return
    elif msg[u'Content'] == 'get':
        if not authority(msg['ActualUserName']):
            itchat.send(u'你不是gm', msg['FromUserName']) 
            return
        itchat.send(u'%d' % ran, msg['FromUserName']) 
        return
    elif msg[u'Content'] == '愤怒的小脑':
        Lock.acquire()
        global brain
        brain = throwGame(16)
        img = brain.createImg()
        gif.createGIF('brain.gif', img, 256, 256, 0, 0)
        ret = itchat.send_image('brain.gif', msg['FromUserName'])
        itchat.send(u'游戏开始请输入:throw angle fire offset\n角度 火力 位移，如:throw 25 90 10', msg['FromUserName']) 
        Lock.release()
        return
    elif msg[u'Content'] == '报名':
        if nickName == '父母':
            nickName = '隔夜果酱'.decode('utf8')
            print nickName
        strRet = WOLF.sign(nickName)
        itchat.send(u'%s' % strRet, msg['FromUserName']) 
        return
    img, strResp = planeGame.parse(data, msg['ActualNickName'])
    if strResp:
        if type(strResp) == list:
            for i in range(len(img)):
                if img[i]:
                    Lock.acquire()
                    gif.createGIF('plane.gif', img[i], 256, 256, 0, 0)
                    ret = itchat.send_image('plane.gif', msg['FromUserName'])
                    Lock.release()
                itchat.send(u'%s' % strResp[i], msg['FromUserName'])  
        else:
            itchat.send(u'%s' % strResp, msg['FromUserName'])   
        return
    
    strResp = guess.parse(msg[u'Content'], nickName, msg)
    if strResp:
        itchat.send(u'%s' % (strResp), msg['FromUserName'])  
        return  

    try:
        filtStr = filt.filter(msg['Content'])
        if filtStr:
            num = random.randint(0, 10)
            if num < 5:
                itchat.send(u'%s' % (filtStr), msg['FromUserName'])
                return
    except KeyError:
        print 'keyError'

    num = random.randint(0, 20)
    print num
    if num == 1:
        recvMsg = msg['Content']
        recv = robotChat(recvMsg, 1)
        itchat.send(u'%s' % (recv), msg['FromUserName'])           
            
            
                    
def notifyMe(data):
    try:
        me = itchat.search_friends(remarkName='父母')
        if me:
            for i in me:
                userName = i['UserName']
                itchat.send(u'%s' % (data), userName)
    except KeyError:
        print 'keyError'
def notifyAll(info):
    flag = info[5]
    if flag[1] == '0':
        d = datetime.datetime.now()
        week = str(d.weekday() + 1)
        if week not in info[2]:
            return
        if flag[2] == '0':
            contact.notifyAll(info[4])
        else:
            recv = robotChat(info[4], 1)
            contact.notifyAll(recv)
        if flag[0] == '0':
            DB.allDelete(info[0])
    elif flag[1] == '1':
        timeStr = time.strftime('%m%d')
        if timeStr != info[2]:
            return
        if flag[2] == '0':
            contact.notifyAll(info[4])
        else:
            recv = robotChat(info[4], 1)
            contact.notifyAll(recv)
        if flag[0] == '0':
            DB.allDelete(info[0])
        
            
        
def timeFunc():     
    while(1):
        #now = time.localtime(time.time())
        timeStr = time.strftime('%H%M')
        result = DB.query(timeStr)
        for i in result:
            notifyMe('%s:%s' % (i[1], i[2]))
            if i[3] == 0:
                DB.delete(i[0])
        #if now.tm_hour == 22 and now.tm_min == 0:
            #recv = robotChat('明天天气怎么样', 1)
            #notifyMe(recv)
        #elif now.tm_hour == 6 and now.tm_min == 30:
            #recv = robotChat('今天天气怎么样', 1)
            #notifyMe(recv)
        
        result = DB.allQuery(timeStr)
        for i in result:
            notifyAll(i)
        time.sleep(59)          

def watchFun():
    while(1):
        print 'thread go'
        t = threading.Thread(target=timeFunc)
        t.start()
        t.join()
        time.sleep(60)
watchDog = threading.Thread(target=watchFun)
watchDog.start()
itchat.auto_login(True)
itchat.run()
print 'will close'
DB.close()
