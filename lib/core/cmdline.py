#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from lib.core.log import loger
from lib.core.common import checkSystemEncoding
from lib.core.common import getUnicode
from optparse import OptionParser
from optparse import OptionGroup




def cmdLineParser(argv=None):
    argItem = {}
    if argv==None:
        argv=sys.argv
    checkSystemEncoding()
    _ = getUnicode(os.path.basename(argv[0]), encoding=sys.getfilesystemencoding() or "utf8")

    usage = "%s%s [options]" % ("Python " ,
            "\"%s\"" % _)

    parser = OptionParser(usage=usage)

    parser.add_option('-v',"--version", dest="showVersion", action="store_true",help="Show program's version number and exit")
    # Target options
    target = OptionGroup(parser, "Target", "At least one of these options has to be provided to define the target(s)")
    target.add_option("-u","--url",dest="Url",help="被检测的URL")
    parser.add_option_group(target)
    options, args=parser.parse_args()
    if options.Url==None:
        parser.error("Please input key parameters")
        return {}

    for i in parser.defaults:                    #获取所有参数
        argItem[i]=getattr(options,i)
    return argItem









