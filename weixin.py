#coding=utf8
import urllib2
import urllib
import itchat
from itchat.content import *
import sys  
from magnet import getAllMagnet
import re
reload(sys)  
sys.setdefaultencoding('utf8')   
def post(data):
    #data=urllib.quote_plus(data)
    url = 'http://60.205.206.18/?signature=58a37c24b16f9f442d8854f44edaf85d0687183b&timestamp=1480424201&nonce=2011091517&openid=o1zOPuInKqVUN-7ILHP49CVEIIzs'
    data = '<xml><ToUserName><![CDATA[gh_2e3470ff053c]]></ToUserName><FromUserName><![CDATA[123]]></FromUserName><CreateTime>1480427536</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[' + data + ']]></Content><MsgId>6358387851629769718</MsgId></xml>'
    req = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(req)
    return response.read()
def robotChat(data):
    url='http://openapi.tuling123.com/openapi/api/v2'
    data = data.encode("utf-8")
    data = '{"perception":{"inputText":{"text":"' + data + '"},"selfInfo":{"location":{"city":"杭州","latitude":"30.26","longitude":"120.19","nearest_poi_name":"大华股份","province":"浙江","street":"滨安路"},}},"userInfo":{"apiKey":"bd7514ba69cf46ab9669c07e3a1ce440","userId":41234}}'
    req = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(req)
    resp = response.read()
    startStr = '"values":{"text":"'
    start = resp.index(startStr)
    end = resp.index('"}}]}')
    return resp[start + len(startStr):end]

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print 'text_reply:' 
    print msg
    recv = robotChat(msg['Text'])
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


# 在注册时增加isGroupChat=True将判定为群聊回复
@itchat.msg_register(TEXT, isGroupChat = True)
def groupchat_reply(msg):
    print 'groupchat_reply:' 
    print msg
    print msg['ActualNickName']
    print msg['FromUserName']
    data = msg['Content'].encode("utf-8")
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
                    

itchat.auto_login(True)
itchat.run()