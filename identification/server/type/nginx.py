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

    list=[serverNum,dateNum,contenttypeNum,contentlengthNum,connectionNum]
    try:
        list.remove(-1)
    except:
        pass
    if sorted(list) == list:
        retval=True
        webServer.type='Nginx'

    if retval:
        respHeaders = getResponseHeaders(url,mode="PUT")
        if respHeaders.code=="411 Length Required".lower():
            webServer.version= "0.7.69-1.3.9"
        elif getResponseHeaders(url,mode="0d9y").code=="".lower():
            webServer.version= "1.4.0-1.5.4"
        elif getResponseHeaders(url,mode="0d9y").code=="400 Bad Request".lower():
            webServer.version = "1.5.5-Now"
        else:
            webServer.version = "Unknown"

