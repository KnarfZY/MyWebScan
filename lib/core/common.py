#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import socket
import codecs
import urllib2
import ssl
from urlparse import urlparse

from lib.core.datatype import AttribDict
from lib.core.settings import paths
from lib.core.settings import headers
from lib.core.log import loger

def isFrozen():
    """
    查看是否被打包成了exe文件
    """
    return hasattr(sys, "frozen") #检测sys里面是否可以调用frozen参数

def getUnicode(value, encoding=None, ToNull=False):
    """
    解码成unicode
    """

    if ToNull and value is None:
        return "NULL"

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):  #说明value是str类型
        while True:
            try:
                return unicode(value, encoding  or "utf8")
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, "utf8")  #将str通过utf8解码成unicode
                except:
                    value = value[:ex.start] + "".join(r"\x%02x" % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    elif isListLike(value):
        value = list(getUnicode(_, encoding, ToNull) for _ in value)
        return value
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # 忽略错误，先变成str再次用ASCII解码

def isListLike(value):
    return isinstance(value,(list,tuple,set))

def setPaths(rootPath):
    paths.WEBSCAN_ROOT_PATH = rootPath
    # webscan paths
    paths.WEBSCAN_LIB_PATH=os.path.join(paths.WEBSCAN_ROOT_PATH,"lib")
    paths.WEBSCAN_IDENTIFICATION_PATH = os.path.join(paths.WEBSCAN_ROOT_PATH, "identification")
    paths.WEBSCAN_SERVER_PATH = os.path.join(paths.WEBSCAN_IDENTIFICATION_PATH, "server")
    paths.WEBSCAN_SERVERTYPE_PATH=os.path.join(paths.WEBSCAN_SERVER_PATH,"type")

    paths.WEBSCAN_CMS_PATH = os.path.join(paths.WEBSCAN_IDENTIFICATION_PATH, "cms")
    paths.WEBSCAN_CMSTYPE_PATH=os.path.join(paths.WEBSCAN_CMS_PATH,"type")



def checkSystemEncoding():
    """
    检查系统的编码
    """

    if sys.getdefaultencoding() == "cp720":
        try:
            codecs.lookup("cp720")
        except LookupError:
            errMsg = "there is a known Python issue (#1616979) related "
            errMsg += "to support for charset 'cp720'. Please visit "
            errMsg += "'http://blog.oneortheother.info/tip/python-fix-cp720-encoding/index.html' "
            errMsg += "and follow the instructions to be able to fix it"
            loger.error(errMsg)

            warnMsg = "temporary switching to charset 'cp1256'"
            loger.error(warnMsg)

            reload(sys)
            sys.setdefaultencoding("cp1256")


def getResponse(req,redirect=False):
    if type(req)==str:
        req = req if urlparse(req).scheme != "" else "http://" + req
    try:
        resp=urllib2.urlopen(req,timeout=4)
        while resp.code==302 and redirect:
            print resp.headers
            resp=urllib2.urlopen(resp.headers["Location"],timeout=4)
        return resp
    except urllib2.HTTPError, e:
        return e
    except:
        e=AttribDict()
        e.code=404
        return e






def getRequest(url,headers={},data={}):
    url = url if urlparse(url).scheme != "" else "http://" + url
    try:
        if data:
            return urllib2.Request(url,headers=headers,data=data)
        else:
            return urllib2.Request(url, headers=headers)
    except:
        return url

def getResponseHeaders(url,Agreement="HTTP/1.0",mode="GET"):
    #返回response中headers的排序list和code (均小写)
    try:
        parse=urlparse(url)
        url=url if parse.scheme!="" else "http://"+url
        if parse.scheme=="http":

            http=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            http.settimeout(3)
            http.connect((parse.hostname, parse.port if parse.port else 80))
        else:
            http=ssl.wrap_socket(socket.socket())
            http.settimeout(3)
            http.connect((parse.hostname, 443))
        parse = urlparse(url)
        message='{0} {1} {2}\r\nHost: {3}\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36\r\nAccept: */*\r\nConnection: close\r\n\r\n'
        path=parse.path+(("?"+parse.query ) if parse.query else "" if parse.path else "/")
        message=message.format(mode,path,Agreement,parse.hostname)
        http.send(message)
        response = http.recv(2048)
        response=  response.lower()
        http.close()
        headers=AttribDict()
        headers.code=response[response.find(" ")+1:response.find("\r\n")]
        headers.headers=map(lambda x:x.split(":")[0].strip(),response[response.find("\r\n")+2:response.find("\r\n\r\n")].split("\r\n"))
        return headers
    except:
        return False


def loadConvert(input):
    if isinstance(input, dict):
        return {loadConvert(key): loadConvert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [loadConvert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input










