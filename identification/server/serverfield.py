#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.core.common import getResponse
from lib.core.common import getRequest
from lib.core.settings import webServer
from urlparse import urlparse
headers = {'User-Agent':'User-Agent	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'}
def headersServer(url):
    url= url if urlparse(url).scheme!="" else "http://"+url
    url=urlparse(url).scheme+"://"+urlparse(url).netloc
    req=getRequest(url,headers=headers)
    resp=getResponse(req)
    if resp.headers.has_key('Server'):
        if resp.headers['Server'].find('/')!=-1:
            if webServer.has_key('type'):
                if webServer.type==resp.headers['Server'].split("/")[0]:
                    webServer.version=resp.headers['Server'].split("/")[1]
            else:
                webServer.version = resp.headers['Server'].split("/")[1]
                webServer.type = resp.headers['Server'].split("/")[0]
            return True
        else:
            webServer.version = "Unknown"
            webServer.type = resp.headers['Server']
            return True
    else:
        return None



