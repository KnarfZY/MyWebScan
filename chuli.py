import glob

def delnf(filel):
    with open(filel,"r") as ofile:
        txt=ofile.readlines()
    with open(filel,"w") as ofile:
        for line in txt:
            if line.find("NOTFIND")==-1:
                ofile.write(line)
def px(filel):
    ritem={}
    with open(filel,"r") as ofile:
        txt=ofile.readlines()
    for line in txt:
        if ritem.has_key(line):
            ritem[line]=ritem[line]+1
        else:
            ritem[line]=1
    with open(filel,"w") as ofile:
        ofile.write(filel.split("/")[-1]+"\n")
        number=1
        rlist=sorted(ritem.items(), key=lambda x: x[1],reverse=True)
        for key, value in rlist:
            if number==5:
                break
            ofile.write(key)
            number=number+1


if __name__=="__main__":
    for found in glob.glob("cmstype1/*"):
        delnf(found)
        px(found)