#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urlparse import urlparse
from lib.core.common import getResponse
from lib.utils.hyperlink import hyperLink
from lib.core.settings import webOs

def notFindResponse(url):
    url=url if urlparse(url).scheme!="" else "http://"+url
    host=urlparse(url).scheme+"://"+urlparse(url).netloc
    url=host+"/2b6b17d9173a182a4f86e8fa7877d4fb.html"
    return getResponse(url)

def respOs(url):
    url=url if urlparse(url).scheme!="" else "http://"+url
    if urlparse(url).path!="" and getResponse(url).code==200:
        url_lower_response=getResponse(url.lower())
        url_upper_Response = getResponse(url.upper())
        url_response = getResponse(url)
        not_find_response=notFindResponse(url)
        if url_response.code==200:
            if not_find_response.code!=200:
                if url_lower_response.code==url_upper_Response.code==url_response.code:
                    webOs.type={'name':'Window'}
                    return True
                else:
                    webOs.type = {'name': 'Linux'}
                    return True
            elif not_find_response.read()!=url_response.read():
                if url_lower_response.read()==url_upper_Response.read()==url_response.read():
                    webOs.type = {'name': 'Window'}
                    return True
                else:
                    webOs.type = {'name': 'Linux'}
                    return True
            else:
                return None
    else:
        for url in hyperLink(urlparse(url).scheme+"://"+urlparse(url).netloc,js=True,css=True,host=True):
            if urlparse(url).path != "" and getResponse(url).code == 200:
                return respOs(url)
            else:
                return None






