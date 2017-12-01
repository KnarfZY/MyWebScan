#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urlparse import urlparse
from identification.webos.libnmap.process import NmapProcess
from identification.webos.libnmap.parser import NmapParser, NmapParserException
from lib.core.settings import webOs

import socket
def portScan(url):
    url = url if urlparse(url).scheme != "" else "http://" + url
    ip=socket.gethostbyname(urlparse(url).hostname)
    nmproc = NmapProcess(str(ip))
    rc = nmproc.run()
    if rc != 0:
        return None
    try:
        parsed = NmapParser.parse(nmproc.stdout)
        portServer={}
        for host in parsed.hosts:
            for serv in host.services:
                if serv.state=="open" and serv.service != "unknown":
                    portServer[serv.port]=serv.service
            print host.os_match_probabilities()
        webOs.port = portServer
        return True
    except:
        return None

def osScan(url,portScan=False):
    url = url if urlparse(url).scheme != "" else "http://" + url
    ip=socket.gethostbyname(urlparse(url).hostname)
    nmproc = NmapProcess(str(ip),"-O")
    rc = nmproc.sudo_run()
    if rc != 0:
        return None
    try:
        parsed = NmapParser.parse(nmproc.stdout)
        portServer={}
        for host in parsed.hosts:
            for serv in host.services:
                if serv.state=="open" and serv.service != "unknown":
                    portServer[serv.port]=serv.service
            if portScan:
                webOs.type=host.os_match_probabilities()
                webOs.port=portServer
                return True
            else :
                webOs.type = host.os_match_probabilities()
                return True
    except:
        return None







