# -*- coding:UTF-8 -*-
import collections
import os


def run(**args):
    dic = collections.defaultdict()
    info = ""
    #print "[*] In dirlister module."
    path = 'D:/'
    name = str(path).replace('/', '_').replace(':', '')
    print name
    if not os.path.exists(path):
        dic[name] = "not exist\n"
        return dic
    if os.path.isfile(path):
        fp = open(path)
        dic[name] = fp.read()
        fp.close()
        return dic
    files = os.listdir(path)
    path = path + "/"
    for a in files:
        if os.path.isfile(path+a):
            info += a+" -file\n"
            continue
        if os.path.isdir(path+a):
            info += a + " -dir\n"
            continue
        info += a + "-other file\n"
    dic[name] = str(info)
    return dic
run()