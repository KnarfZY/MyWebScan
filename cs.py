#!/usr/bin/env python
# -*- coding: utf-8 -*-

from identification.webos.webfingerprint import respOs
from identification.webos.nmapscan import osScan
from identification.server.serverfield import headersServer
import sys
from lib.utils.hyperlink import hyperLink
import os
from  urlparse import urlparse
from lib.core.common import getResponse
from lib.core.common import getRequest
from lib.core.common import getResponseHeaders

#print dict(getResponse("xmb.0d9y.cn").headers),getResponse("xmb.0d9y.cn").headers
#for i in getResponse("junk://143.130.20.13").info():
#    print i

print osScan("http://www.suda.edu.cn"),respOs("http://www.suda.edu.cn")



