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
from word import WORD
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
'''
gif = gifHelper()
#gif.parseGif('D:\\tmp\\test.gif')
gif.parseGif('D:\\load.gif')

img = throwGame().throw()
gif.createGIF('D:\\out.gif', img, 256, 256, 0, 0)
'''
word = WORD()
WORD.getTrans('apple')
word.getRandom()