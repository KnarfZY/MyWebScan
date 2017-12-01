#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import sys

from lib.core.settings import webServer
from lib.core.settings import paths
from lib.core.log import loger
def respServer(url):
    for found in glob.glob(os.path.join(paths.WEBSCAN_SERVERTYPE_PATH, "*.py")):
        dirname, filename = os.path.split(found)
        dirname = os.path.abspath(dirname)

        if filename == "__init__.py":
            continue

        if dirname not in sys.path:
            sys.path.insert(0, dirname)
        try:
            if filename[:-3] in sys.modules:
                del sys.modules[filename[:-3]]
            module = __import__(filename[:-3].encode(sys.getfilesystemencoding() or "utf-8"))
        except ImportError, msg:
            pass
        if hasattr(module,"detect"):
            try:
                module.detect(url)
            except:
                loger.error("The {0} is error".format(filename[:-3]))
        else:
            errMsg = "missing function 'detect()' "
            loger.error(errMsg)
    if not webServer.has_key('type'):
        return None
    else :
        return True
