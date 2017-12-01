#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True  #不会生成pyc文件


import inspect
import os
import sys
from distutils.version import LooseVersion    #查看python版本
from lib.core.settings import Version
from lib.core.common import isFrozen
from lib.core.common import getUnicode
from lib.core.common import setPaths
from lib.core.cmdline import cmdLineParser
from lib.core.settings import cmdLineOptions
from lib.core.log import loger
from lib.core.settings import webCms
from lib.core.settings import webOs
from lib.core.settings import webServer


def modulePath():
    """
    返回此文本的绝对路径，哪怕文本是相对路径启动。
    os.path.realpath()避免是相对路径启动__file__无法获取到绝对路径的问题
    """
    try:
        _ = sys.executable if isFrozen() else __file__  #如果被打包成exe就用sys.executable（解释器路径），否则用__file__路径
    except NameError:
        _ = inspect.getsourcefile(modulePath) #返回modulePath函数所在的python脚本名字

    return getUnicode(os.path.dirname(os.path.realpath(_)), encoding=sys.getfilesystemencoding() or "utf8")

def checkEnvironment():
    try:
        os.path.isdir(modulePath())
    except UnicodeEncodeError:
        errMsg = "your system does not properly handle non-ASCII paths. "
        errMsg += "Please move the WebScan's directory to the other location"
        loger.error(errMsg)
        raise SystemExit

    if LooseVersion(Version.Version) < LooseVersion("1.0"):
        errMsg = "your runtime environment (e.g. PYTHONPATH) is broken. "
        errMsg += "Please make sure that you are not running newer versions of WebScan with runtime scripts for older versions"
        loger.error(errMsg)
        raise SystemExit
def main():
    checkEnvironment()
    setPaths(modulePath())
    cmdLineOptions.update(cmdLineParser())

    from identification.webos.nmapscan import osScan
    from identification.webos.webfingerprint import respOs
    from identification.server.headers import respServer
    from identification.server.serverfield import headersServer
    from identification.cms.filehash import cmsForceScan
    loger.message("启动")

    osScan(cmdLineOptions.Url,True) or respOs(cmdLineOptions.Url)
    respServer(cmdLineOptions.Url)
    headersServer(cmdLineOptions.Url)
    cmsForceScan(cmdLineOptions.Url)
    loger.info("webServer类型"+webServer.type)
    loger.info("webServer版本" + webServer.version)
    loger.info("webOS类型以及开发端口")
    print webOs
    loger.message("webCms类型"+webCms.type)
    loger.error("结束")



if __name__=="__main__":
    main()



