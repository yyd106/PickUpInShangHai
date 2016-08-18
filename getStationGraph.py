# -*- coding: UTF-8 -*-
import re
import sys
import mimetypes
reload(sys)
sys.setdefaultencoding('utf8')

def ifIsStation (line):
    stationPattern = re.compile(u".*title\W\W([\u4e00-\u9fa5]+)站\W\W[\u4e00-\u9fa5]+.+")
    resultStation = re.match(stationPattern, line)
    if resultStation:
        stationNotPattern1 = re.compile(u".*class.*")
        resultNotStation1 = not re.match(stationNotPattern1, line)
        if resultNotStation1:
            stationNotPattern2 = re.compile(u'.*rowspan.*')
            resultNotStation2 = not re.match(stationNotPattern2, line)
            if resultNotStation2:
                stationName = resultStation.group(1)
#                print stationName
                return stationName
    return ""

def ifIsNewLine (line, lastLine):
    linePattern = re.compile(u".*700px.*[\u4e00-\u9fa5]{6}(\d*)[\u4e00-\u9fa5]{4}.*")
    lineResult = re.match(linePattern, line)
    if lineResult:
#        print line
        nextLine = lineResult.group(1)
        return nextLine
    return lastLine


def getTheStationGraph():
    f = open('ShangHai.xml', 'r')
    stationGraph = {}
    mime = mimetypes.guess_type('ShangHai.xml')
    print mime
#    lines = f.readline().decode('utf-8')
    lastLine = 0
    nextLine = 0
    lastStation = ""
    nextStation = ""

    while 1:
        line = f.readline().decode('utf-8')
#        print line
        if not line:
            break
        nextLine = ifIsNewLine(line, lastLine)
        if nextLine and nextLine != lastLine:
            lastLine = nextLine
            lastStation = ""
#            print lastLine
        nextStation = ifIsStation(line)
        if nextStation:
            if not stationGraph.has_key(nextStation):
                stationGraph[nextStation] = []
            if lastStation:
                stationGraph[nextStation].append(lastStation)
                stationGraph[lastStation].append(nextStation)
#                print stationGraph[nextStation][0].encode("utf-8")
            lastStation = nextStation
    return stationGraph

#    if nextStation and lastStation:

if __name__=="__main__":
    stationGroup = getTheStationGraph()
    print stationGroup
