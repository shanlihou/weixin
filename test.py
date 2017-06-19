#coding=utf8
import urllib2
import urllib
from DBHelper import DBHelper
import os
from wxRequest import wxRequest
from filter import filtHelper
import json
import datetime
from guessNumber import guessNumber
import random
from gifHelper import gifHelper
from throwGame import throwGame
from wolf import wolf
from plane import plane
from readData import readData
from planeHelper import planeHelper
from jpgHelper import jpgHelper
from betHelper import betHelper
import math
'''
def post(url, data):
    req = urllib2.Request(url)  
    data = urllib.urlencode(data)  
    #enable cookie  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    response = opener.open(req, data)  
    return response.read()  
	data=urllib.quote_plus(data)
	print data
	req = urllib2.Request(url = url, data = data)
	response = urllib2.urlopen(req)
	return response.read()'''
def post(data):
    data=urllib.quote_plus(data)
    url = 'http://60.205.206.18/?signature=58a37c24b16f9f442d8854f44edaf85d0687183b&timestamp=1480424201&nonce=2011091517&openid=o1zOPuInKqVUN-7ILHP49CVEIIzs'
    data = '<xml><ToUserName><![CDATA[gh_2e3470ff053c]]></ToUserName><FromUserName><![CDATA[123]]></FromUserName><CreateTime>1480427536</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[' + data + ']]></Content><MsgId>6358387851629769718</MsgId></xml>'
    req = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(req)
    return response.read()
data = '<xml><ToUserName><![CDATA[gh_2e3470ff053c]]></ToUserName><FromUserName><![CDATA[123]]></FromUserName><CreateTime>1480427536</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[呢]]></Content><MsgId>6358387851629769718</MsgId></xml>'

def robotChat(data):
    url='http://openapi.tuling123.com/openapi/api/v2'
    data = u'你好'
    data = data.encode("utf-8")  
    print data
    print type(data)
    #data=urllib.quote_plus(data)
    print type(data)
    data = '{"perception":{"inputText":{"text":"' + data + '"},"selfInfo":{"location":{"city":"杭州","latitude":"30.26","longitude":"120.19","nearest_poi_name":"大华股份","province":"浙江","street":"滨安路"},}},"userInfo":{"apiKey":"bd7514ba69cf46ab9669c07e3a1ce440","userId":41234}}'
    req = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(req)
    resp = response.read()
    startStr = '"values":{"text":"'
    start = resp.index(startStr)
    end = resp.index('"}}]}')
    return resp[start + len(startStr):end]
#print robotChat('呢')
db = DBHelper()
print id(db)
db.insert('1544', 'nothing')
db.insert('1544', 'nothing more', 0)
result = db.query('1544')
for i in result:
    print i
    print type(i)
    if i[3] == 0:
        db.delete(i[0])
output = os.popen('dir')
tmp = output.read()
tmpList = [u'name', u'info']
tmp = u'name'
print u'%s' % (tmp.decode("gbk"))
if tmp in tmpList:
    print 'in'
else:
    print 'not in'
print tmp 
print type(tmp)
pre = u'你是谁'
utf8 = pre.encode('utf8')
UTF_8 = pre.encode('gbk')
utf_8 = pre.encode('utf-8')
print utf8,UTF_8,utf_8
if utf8 == UTF_8:
    print '1'
if utf8 == utf_8:
    print '2'
if UTF_8 == utf_8:
    print '3'
'''
filt = filtHelper()
filt.insert('23', 'ckz是我最敬仰的人')
filt.insert('我们', '陈科争是我最敬仰的人')
print filt.get('ckz')
print filt.get('陈科争')
print filt.filter('陈科争是个智障')
result = db.filtQuery()
print type(result)
d = datetime.datetime.now()
print d.weekday()
print type(d.weekday())

guess = guessNumber()
print guess.parse('猜数字', '小名')
for i in range(100):
    guess.parse(str(random.randint(0,999)), str(random.randint(0, 999)))
guess.parse('排行榜', 'xiaogmao')
'''
'''
gif = gifHelper()
#gif.parseGif('D:\\tmp\\test.gif')
#gif.parseGif('D:\\mie.gif')
game = throwGame(16)
img1 = game.createImg()
gif.createGIF('D:\\box.gif', img1, 256, 256, 0, 0)
img2, ret = game.throw(45, 70, 10)
gif.createGIF('D:\\out.gif', img2, 256, 256, 0, 0)
print ret
img2, ret = game.throw(60, 90, 25)
gif.createGIF('D:\\out1.gif', img2, 256, 256, 0, 0)
print ret
img2, ret = game.throw(60, 90, 45)
gif.createGIF('D:\\out1.gif', img2, 256, 256, 0, 0)
print ret
img2, ret = game.throw(60, 90, 80)
gif.createGIF('D:\\out1.gif', img2, 256, 256, 0, 0)
print ret

img2, ret = game.throw(60, 90, 127)
gif.createGIF('D:\\out1.gif', img2, 256, 256, 0, 0)
print ret
'''
wolves = wolf()
wolves.getCurWeek()

gif = gifHelper()
#gif.parseGif('D:\\4.gif')

#game = plane()
'''
img = [game.createFrame()]
for i in range(20):
    print game.getRan()
    game.goChess(0)
    img.append(game.createFrame())
gif.createGIF('D:\\box.gif', img, 256, 256, 0, 0)
'''
'''
img = []
for i in range(20):
    game.getRan()
    img.extend(game.goChess(0))
print len(img)
gif.createGIF('D:\\box.gif', img, 256, 256, 0, 0)
'''
'''
planeGame = planeHelper()
img, strPrint = planeGame.parse('飞行棋', '1')
#img, strPrint = planeGame.parse('飞行棋', '2')
img, strPrint = planeGame.parse('飞行棋开始', '1')
print strPrint
count = 0

while 1:
    #strRet = raw_input("Enter your input: ")
    name = raw_input("name: ")
    #print strRet
    print name
    img, strPrint = planeGame.parse('fly', name)
    for i in range(len(img)):
        if img[i]:
            count += 1
            gif.createGIF('D:\\box%d.gif' % count, img[i], 256, 256, 0, 0)
        if strPrint[i]:
            print strPrint[i]
'''
'''
for i in range(40):
    if i % 2 == 0:
        img, strPrint = planeGame.parse('fly', '1')
    else:
        img, strPrint = planeGame.parse('fly', '2')         
    if img:
        gif.createGIF('D:\\box%d.gif' % i, img, 256, 256, 0, 0)
    if strPrint:
        print strPrint
'''
bet = betHelper()
bet.setEdge(58, 98)
bet.setEdge(59, 42)
bet.setEdge(543, 5353)
bet.setEdge(4234, 234234)
bet.setEdge(58, 44)
bet.delete(543)
print bet.sort()
print db.printDB('bet')
#getData = readData()
#getData.read('D:\\tmp\\Core\\weixin-master\\weixin-master\\plane.txt')
#jpg = jpgHelper('D:\\timg.jpg')
#jpg.parser()
