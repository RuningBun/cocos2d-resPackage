#!/usr/bin/env python
# coding=utf8
"""从文件夹中取出对应的类型的数据"""

import os
import sys
import re
import time
import json
import shutil

version = "v1.1.0.1"
since = "2017-2-20"
# python工程所在的目录
pythonPath = "packageRes"
projectPath = "(packageRes).*?$"
# 输入的路径
writePath = "";
# 项目所在的路径
projectRes = "res"
# 创建一个新的存放文件夹
newRes = "src/packageRes"
# 散图
pngNoPlist = "pngWithNoPlist.js"
# 散图名称
pngObjName = "_GamePngNames"
# plist名称
pngWithPlist = "pngWithPlist.js"
# 散图名称
plistObjName = "_GamePlistNames"
# 属性过滤文件夹
folderRE = "^.*?\/(\.svn|\.DS_Store).*?$"
# res路径的正则
Res = "^.*?(res)"
# res路径之后
AfRes = "(res).*?$"
# 文件后缀名列表,正则表达式
suffixRE = "^.*?\.(jpg|jpeg|bmp|gif|png)$"
# 保留文件后缀列表,正则表达式
rejectionRE = "^.*?\.(plist)$"
# plist内部的key
plistKey = '<key>(.*).png</key>'
# 创建一个集合 存放已经处理的plist 文件名
plistList = []
# 统计散图的数量
global PngWithNoPlsitNum
PngWithNoPlsitNum = 0


def GetFileNameAndExt(filename):
    (filepath, tempfilename) = os.path.split(filename);
    (shotname, extension) = os.path.splitext(tempfilename);
    return shotname,


def eachPngFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if re.match(folderRE, child): continue
        if os.path.isdir(child):
            eachPngFile(child)
        elif re.match(suffixRE, child):
            # 去掉图片的后缀名
            pngName = os.path.splitext(allDir)[0]
            if pngName not in plistList:
                writePngToFile(child, pngName, allDir)


def eachPlistFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if re.match(folderRE, child): continue
        if os.path.isdir(child):
            eachPlistFile(child)
        elif re.match(rejectionRE, child):
            nameList = GetFileNameAndExt(child)
            plistList.append(nameList[0])
            writePlistToFile(child, nameList[0])


def init_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def printData(fileName, title):
    with open(fileName, "a") as resultFile:
        resultFile.write("\t" + title + ":\"" + title + ".png\",//" + "\n")


def getPlistData(writeFilePath, plistPath, plistName):
    with open(plistPath) as plistfile:
        lines = plistfile.readlines()
        patternKeyname = re.compile(plistKey)
        for line in lines:
            if patternKeyname.search(line):
                pngName = patternKeyname.search(line).groups()[0]
                printData(writeFilePath, pngName)


def writePlistToFile(plistPath, plistName):
    # 项目资源所在的路径
    plistPackagePath = os.path.dirname(plistPath) + "/"
    plistPackagePath = plistPackagePath.replace(projectRes, newRes)
    if not os.path.exists(plistPackagePath):
        os.makedirs(plistPackagePath)
    writeFilePath = plistPackagePath + plistName + ".js"
    init_file(writeFilePath)
    with open(writeFilePath, "a") as resultFile:
        resultFile.write("_" + plistName + "={" + "\n")
    getPlistData(writeFilePath, plistPath, plistName)
    with open(writeFilePath, "a") as resultFile:
        resultFile.write("};")

    plistfilePath = writePath + pngWithPlist
    strinfo = re.compile(Res)
    newPngPath = strinfo.sub("res", plistPath)
    with open(plistfilePath, "a") as resultFile:
        resultFile.write("\t" + plistName + ":\"" + newPngPath + "\",//\n")


def writePngToFile(pngPath, pngName, fullPngName):
    pngPackagePath = os.path.dirname(pngPath) + "/"
    strinfo = re.compile(Res)
    newPngPath = strinfo.sub("res", pngPackagePath)
    newPngName = newPngPath + fullPngName;
    writepath = writePath + pngNoPlist
    global PngWithNoPlsitNum
    PngWithNoPlsitNum += 1
    with open(writepath, "a") as resultFile:
        resultFile.write("\t" + pngName + ":\"" + newPngName + "\",//\n")


def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


if __name__ == "__main__":
    # 找到脚本文件所在的项目目录
    PngWithNoPlsitNum = 0
    pythonFilePath = cur_file_dir()
    print pythonFilePath
    strinfo = re.compile(projectPath)
    filesPath = strinfo.sub("res", pythonFilePath)
    print filesPath

    writePath = os.path.dirname(filesPath) + "/" + newRes + "/";
    if os.path.exists(writePath):
        shutil.rmtree(writePath)
    os.makedirs(writePath)

    plistwithpngPath = writePath + pngWithPlist
    if not os.path.isfile(plistwithpngPath):
        with open(plistwithpngPath, "a") as resultFile:
            resultFile.write(plistObjName + "={" + "\n")
    eachPlistFile(filesPath)
    if os.path.isfile(plistwithpngPath):
        with open(plistwithpngPath, "a") as resultFile:
            resultFile.write("};")

    writepath = writePath + pngNoPlist
    if not os.path.isfile(writepath):
        with open(writepath, "a") as resultFile:
            resultFile.write(pngObjName + "={" + "\n")
    eachPngFile(filesPath)
    # 在遍历的最后才添加括号
    if os.path.isfile(writepath):
        with open(writepath, "a") as resultFile:
            resultFile.write("};")

    print "================================================================="
    print "=============================资源文件生成完毕======================="
    print "PngWithNoPlist:\t\t %d \t\t" % PngWithNoPlsitNum
    print "PngWithPlist:\t\t %d \t\t" % len(plistList)
    print "===================== GOOD LUCK && ENJOY IT ====================="
