#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import ssl
import json
import os
from identification.cms.filehash import cmsForceScan
import threading
from lib.core.common import setPaths
import time



gtoken="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ik5vbmUiLCJ1dWlkIjoiOWQzMDliODZjMmRmZmI1MjBiOTVjMWQyNDFmMzEwMTUiLCJpYXQiOjE1MTE3NjU0NjYsImV4cCI6MTUxMTg1MTg2Nn0.L0DFaXkEIJYURtuEpbEwN8XLyqGOS2r5k9DhZf-3pxQ"
def token():
    http = ssl.wrap_socket(socket.socket())
    http.settimeout(3)
    http.connect(('sso.telnet404.com', 443))
    message="""GET /cas/login?service=https%3A%2F%2Fwww.zoomeye.org%2Flogin HTTP/1.1
Host: sso.telnet404.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://www.zoomeye.org/login
Cookie: __jsluid=65db0a2ff41bf6de7061ec6943bd682f; __jsl_clearance=1511596159.58|0|ojtpCsAD0v%2Fzg%2FdpuC5vZ60PG3U%3D; Hm_lvt_3c8266fabffc08ed4774a252adcb9263=1511596165,1511596233; Hm_lpvt_3c8266fabffc08ed4774a252adcb9263=1511596233
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1
\r\n
"""
    http.send(message)
    temp = http.recv(1024)
    resp = ""
    while temp:
        resp = resp + temp
        temp = http.recv(1024)
    print resp[resp.find("\r\n\r\n"):].strip()
    rjson = json.loads(resp[resp.find("\r\n\r\n"):].strip())
    global gtoken
    gtoken=rjson['token']

def search(cmstype="",page=1):
    http=ssl.wrap_socket(socket.socket())
    http.settimeout(3)
    http.connect(('www.zoomeye.org', 443))

    search='app:"%s"'%(cmstype)
    page=page
    message="""GET /api/search?q={0}&p={1} HTTP/1.1
Host: www.zoomeye.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0
Accept: application/json, text/plain, */*
Accept-Language: zh,en-US;q=0.7,en;q=0.3
Cube-Authorization: {2}
Referer: https://www.zoomeye.org/searchResult?q=app%3A%27dedecms%27
Cookie: __jsluid=65db0a2ff41bf6de7061ec6943bd682f; __jsl_clearance=1511596159.58|0|ojtpCsAD0v%2Fzg%2FdpuC5vZ60PG3U%3D; Hm_lvt_3c8266fabffc08ed4774a252adcb9263=1511596165,1511596233; Hm_lpvt_3c8266fabffc08ed4774a252adcb9263=1511596385
DNT: 1
Connection: close
\r\n
    """.format(search,page,gtoken)
    http.send(message)
    temp=http.recv(1024)
    resp=""
    while temp:
        resp=resp+temp
        temp=http.recv(1024)
    print resp[resp.find("\r\n\r\n"):].strip()
    rjson=json.loads(resp[resp.find("\r\n\r\n"):].strip())
    print rjson
    _list=[]
    for matchs in rjson['matches']:
        try:
            _list.append(matchs['webapp'][0]['url'])
        except:
            _list.append(matchs['portinfo']['service']+u"://"+matchs['ip'])
    return _list



cmstype="思途CMS"
dedecmsurl_list=[]

with open("%s.txt"%(cmstype),"a+") as dedecms:
    dedecms.seek(0)
    for url in dedecms:
        dedecmsurl_list.append(str(url.strip()))
with open("%s.txt"%(cmstype),"a+") as dedecms:
    setPaths((os.path.dirname(os.path.realpath(__file__))))
    for i in xrange(1,100):
        for url in search(cmstype,i):
            if str(url) in dedecmsurl_list:
                continue
            print url
            dedecmsurl_list.append(str(url))
            dedecms.write(str(url)+"\n")
            print     dedecms.tell()
            try:
                cmsForceScan(str(url),cmstype)
            except:
                pass

