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
from contacts import contacts
#from logWeixin import logWeixin
from DBHelper import DBHelper
from filter import filtHelper
import datetime
reload(sys)  
sys.setdefaultencoding('utf8')  
DB = DBHelper() 
contact = contacts()
filt = filtHelper()
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
def robotChat(data):
    url='http://openapi.tuling123.com/openapi/api/v2'
    data = data.encode("utf-8")
    data = '{"perception":{"inputText":{"text":"' + data + '"},"selfInfo":{"location":{"city":"杭州","latitude":"30.26","longitude":"120.19","nearest_poi_name":"大华股份","province":"浙江","street":"滨安路"},}},"userInfo":{"apiKey":"bd7514ba69cf46ab9669c07e3a1ce440","userId":41234}}'
    req = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(req)
    resp = response.read()
    stJson = json.loads(resp)
    print 'resp:'
    print resp
    print 'strJson:\n'
    print stJson
    '''
    startStr = '"values":{"text":"'
    start = resp.index(startStr)
    end = resp.index('"}}]}')
    return resp[start + len(startStr):end]'''
    strRet = ''
    print '\n\n\n\nwill go:\n'
    strRet = parseJson(stJson)
    print strRet
    return strRet

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print 'text_reply:' 
    print msg
    recv = robotChat(msg['Text'])
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
    print data
    userInfo = itchat.search_chatrooms(userName = msg['FromUserName'])
    wx_id = userInfo[u'Uin']
    contact.push(wx_id, msg['FromUserName'])
    filtStr = filt.filter(msg['Content'])
    if filtStr:
        itchat.send(u'%s' % (filtStr), msg['FromUserName'])
    if msg['isAt']:
        lenStr = len(u'@鱼塘助手 ')
        recvMsg = msg['Content'][lenStr:]
        recv = robotChat(recvMsg)
        itchat.send(u'%s' % (recv), msg['FromUserName'])
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
        notify = data.split(' ')
        print notify
        if notify[1].isdigit() and len(notify[1]) == 4:
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
        if len(opt) >= 4 and opt[1].isdigit() and opt[2].isdigit() and len(opt[1]) <= 7 and len(opt[2]) == 4:
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
        if len(opt) >= 4 and opt[1].isdigit() and opt[2].isdigit() and len(opt[1]) == 4 and len(opt[2]) == 4:
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
        if len(opt) == 3:
            if opt[1] == 'delete':
                filt.delete(opt[2])
                itchat.send(u'删除成功', msg['FromUserName']) 
                return 
            filt.insert(opt[1], opt[2])
            itchat.send(u'添加操作成功', msg['FromUserName']) 
            return 
        itchat.send(u'操作失败', msg['FromUserName']) 
    elif data.startswith('print'):
        opt = data.split(' ')
        if len(opt) == 2:
            print 'opt 1:' + opt[1]
            if opt[1] == 'notify' or opt[1] == 'notify_all':
                print opt[1]
                strRet = DB.printDB(opt[1])
                print strRet
                itchat.send(u'%s' % (strRet.decode('UTF-8')), msg['FromUserName']) 
                return 
        itchat.send(u'操作失败', msg['FromUserName']) 
    elif data.startswith('delete'):
        opt = data.split(' ')
        if len(opt) == 3 and opt[2].isdigit():
            if opt[1] == 'notify':
                DB.delete(opt[2])
            elif opt[1] == 'notify_all':
                DB.allDelete(opt[2])
            itchat.send(u'操作成功', msg['FromUserName']) 
            return 
        itchat.send(u'操作失败', msg['FromUserName']) 
                
            
            
                    
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
    type = info[5]
    if type[1] == '0':
        d = datetime.datetime.now()
        week = str(d.weekday())
        if week not in info[2]:
            return
        if type[2] == '0':
            itchat.send(u'%s' % (info[4]), contact.getUserName(info[1]))
        else:
            recv = robotChat(info[4])
            itchat.send(u'%s' % (recv), contact.getUserName(info[1]))
        if type[0] == '0':
            DB.allDelete(info[0])
    elif type[1] == '1':
        timeStr = time.strftime('%m%d')
        if timeStr != info[2]:
            return
        if type[2] == '0':
            itchat.send(u'%s' % (info[4]), contact.getUserName(info[1]))
        else:
            recv = robotChat(info[4])
            itchat.send(u'%s' % (recv), contact.getUserName(info[1]))
        if type[0] == '0':
            DB.allDelete(info[0])
        
            
        
def timeFunc():     
    while(1):
        now = time.localtime(time.time())
        timeStr = time.strftime('%H%M')
        result = DB.query(timeStr)
        for i in result:
            notifyMe('%s:%s' % (i[1], i[2]))
            if i[3] == 0:
                DB.delete(i[0])
        if now.tm_hour == 22 and now.tm_min == 0:
            recv = robotChat('明天天气怎么样')
            notifyMe(recv)
        elif now.tm_hour == 6 and now.tm_min == 30:
            recv = robotChat('今天天气怎么样')
            notifyMe(recv)
        
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