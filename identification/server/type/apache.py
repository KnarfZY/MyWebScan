#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.core.settings import  webServer
from lib.core.common import getResponseHeaders

def detect(url):
    retval = False
    respHeaders=getResponseHeaders(url,mode="HEAD")
    try:
        serverNum=respHeaders.headers.index('server')
    except:
        serverNum=-1
    try:
        dateNum=respHeaders.headers.index('date')
    except:
        dateNum=-1
    try:
        connectionNum = respHeaders.headers.index('connection')
    except:
        connectionNum=-1
    try:
        contentlengthNum = respHeaders.headers.index('content-length')
    except:
        contentlengthNum=-1
    try:
        contenttypeNum = respHeaders.headers.index('content-type')
    except:
        contenttypeNum=-1

    list=[dateNum,serverNum,contentlengthNum,connectionNum,contenttypeNum]
    try:
        while -1 in list:
            list.remove(-1)
    except:
        pass
    if sorted(list) == list:
        retval=True
        webServer.type='Apache'

    if retval:
        respHeaders = getResponseHeaders(url,mode="HEAD",Agreement="0D9Y/1.1")
        if respHeaders.code=="400 Bad Request".lower():
            webServer.version= "1.3.X"
        elif respHeaders.code=="200 OK".lower():
            webServer.version= "2.X"
        else:
            webServer.version = "Unknown"
