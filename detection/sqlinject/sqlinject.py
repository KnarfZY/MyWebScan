#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.core.settings import layer
from lib.utils.hyperlink import hyperLink

def layerLink(url):
    def inString(str1,list):
        print str1
        for str2 in list:
            if str1.find(str2)!=-1:
                return True
        return False

    tempLink=[[]for i in xrange(layer+1)]
    allLink=[]
    tempLink[0]=hyperLink(url, host=True)
    allLink.extend(tempLink[0])
    for num in xrange(layer):
        print tempLink[num]
        for link in tempLink[num]:
            tempLink[num+1].extend(hyperLink(link, host=True))
        tempLink[num + 1]=list(set(tempLink[num+1]))
        allLink.extend(tempLink[num+1])
    return [link for link in allLink if inString(link,['aspx?','asp?','php?','jsp?'])]

layerLink('www.baidu.com')