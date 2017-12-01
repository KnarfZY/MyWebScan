#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import json
import hashlib
import os
from urlparse import urlparse
from urlparse import urljoin
from lib.core.common import getResponse
from lib.core.common import getRequest
from lib.core.common import  loadConvert
from lib.core.settings import headers
from lib.core.settings import webCms
from lib.core.settings import paths
from lib.core.datatype import Trie
from lib.utils.hyperlink import hyperLink

def cmsForceScan(url,cmstxt="*"):#查看哪一些cms比较多

    url=(urlparse(url).scheme+"://"+urlparse(url).netloc) if urlparse(url).scheme!="" else ("http://"+ urlparse("http://"+url).netloc)
    print url
    for cms in glob.glob(os.path.join(paths.WEBSCAN_CMSTYPE_PATH,cmstxt+".txt")):
            ofile=open(cms,"r")
            type=ofile.readline()
            root=Trie(loadConvert(json.loads(ofile.read())))
            root.type=type
            root.url=url
            for cmslist in root.getPath():
                try:
                    fileurl,md5hash=cmslist.split(" ")
                    md5=hashlib.md5()
                    resp=getResponse(getRequest(urljoin(url,fileurl),headers=headers))
                    md5.update(resp.read())
                    if resp.code==200 :
                        if md5.hexdigest()==md5hash:
                            webCms.type = root.type
                            return None
                except:
                    pass
    webCms.type = "Unknown"
    return None

def cmsScan(url):
    url=(urlparse(url).scheme+"://"+urlparse(url).netloc) if urlparse(url).scheme!="" else ("http://"+ urlparse(url).netloc)
    url=url.strip("/")

    root=Trie()
    root.url = url
    _list=[]
    for link in hyperLink(root.url, link=False, css=True, js=True, host=True):
        try:
            md5 = hashlib.md5()
            md5.update(getResponse(getRequest(link, headers=headers)).read())
            _list.append(urlparse(link).path + " " + md5.hexdigest())
        except:
            pass
    #print _list
    for cms in glob.glob(os.path.join(paths.WEBSCAN_CMSTYPE_PATH,"*.txt")):
        ofile=open(cms,"r")
        type=ofile.readline().strip()
        root.root=loadConvert(json.loads(ofile.read()))
        root.type=type
        #print root.getPath(not404=False)
        if list(set(root.getPath(not404=False))&set(_list)):
            webCms.type=root.type
            return True
    return False

