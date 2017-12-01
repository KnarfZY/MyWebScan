#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.core.datatype import AttribDict
#软件版本等信息
class Version:
    Version = "1.0"

layer=4
thread=30
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':'User-Agent	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'}
cmdLineOptions=AttribDict()
paths=AttribDict()
webServer=AttribDict()
webOs=AttribDict()
webCms=AttribDict()