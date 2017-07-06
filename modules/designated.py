# -*- coding:UTF-8 -*-
from github3 import login
import fnmatch
import os
import collections


def run(**args):
    type = '.txt'
    dic = collections.defaultdict()
    path = "D:/test/"

    for parent, directories, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*%s" % type):
            document_path = os.path.join(parent, filename)
            fp = open(document_path, "rb")
            document_path = str(document_path).replace('/', '_').replace(':', '').replace('\\', '_')
            dic[document_path] = fp.read()
            fp.close()
    return dic
