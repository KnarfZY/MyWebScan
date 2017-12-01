#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.core.settings import cmdLineOptions
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

    list=[contentlengthNum,contenttypeNum,serverNum,dateNum,connectionNum]
    try:
        list.remove(-1)
    except:
        pass
    if sorted(list) == list:
        retval=True
        webServer.type='Microsoft-IIS'

    if retval:
        respHeaders = getResponseHeaders(url,mode="DELETE")
        if respHeaders.code=="501 Not Implemented".lower():
            webServer.version= "6.0"
        elif respHeaders.code=="405 Method Not Allowed".lower():
            webServer.version= "7.0-Now"
        else:
            webServer.version = "Unknown"
