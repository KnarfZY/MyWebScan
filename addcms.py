#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading
import glob
import hashlib
mkdir="/Users/jianhaoliu/Desktop/cms"
def bl(mkdir,cmstype,sc):
    txt=""
    for found in glob.glob(os.path.join(mkdir,"*")):
        if not os.path.isfile(found):
            bl(found,cmstype,sc)
            continue
        suffix=os.path.basename(found).split(".")[-1]
        if any(suffix==a for a in ["robots.txt","js","css"]):
            file=open(found, "r")
            md5=hashlib.md5()
            md5.update(file.read())
            txt =txt + found[found.find(sc)+len(sc):]+" "+md5.hexdigest()+"\n"
            file.close()
    file=open("identification/cms/type/"+cmstype+".txt","a+")
    file.write(txt)
    file.close()


def foundindex(mkdir):
    if glob.glob(os.path.join(mkdir, "index.*")):
        bl(mkdir,os.path.basename(mkdir),mkdir)
    else:
        for found in glob.glob(os.path.join(mkdir, "*")):
            if os.path.isdir(found):
                if glob.glob(os.path.join(found, "index.*")):
                    bl(found, os.path.basename(mkdir), found)

def zhenghe(mkdir):
    for found in glob.glob(os.path.join(mkdir,"*")):
        if found.split('-')[0] != found:
            file = open("-".join(found.split('-')[:-1]) + ".txt", "a+")
            file.seek(0, 0)
            fileread=file.read()
            with open(found, 'r') as f:
                for txt in f.readlines():
                    if fileread.find(txt.strip()) == -1:
                        file.writelines(txt)
            file.close()
            os.remove(found)
        else:
            continue




if __name__=="__main__":
    ''' 文件夹添加时使用
    #global mkdir
    #os.mkdir("identification/cms/type")
    linklist=[]
    threadlist=[]
    for found in glob.glob(os.path.join(mkdir,"*")):
        linklist.append(found)
    while  linklist:
        for i in xrange(5):
            if linklist:
                t = threading.Thread(target=foundindex, args=(linklist.pop(),))
                threadlist.append(t)
                #t.daemon=True
                t.start()
    for t in threadlist:
        t.join()
    zhenghe("identification/cms/type") 
    '''
    from lib.core.datatype import Trie
    import json
    for found in glob.glob(os.path.join('identification/cms/type', "*.txt")):
        root = Trie()
        root.root = {}

        with  open(found, "r") as txt:
            for line in txt.readlines():
                line = line.split(" ")
                temp = line[0][1:].split("/")
                temp.append(line[1].strip())
                root.insert(temp)

        with open(found,"w") as file:
            file.write(".".join(os.path.basename(found).split(".")[:-1])+"\n"+json.dumps(root.root))

