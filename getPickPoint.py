# -*- coding: UTF-8 -*-

from getStationGraph import getTheStationGraph

def initialDistanceMatrix(stationGroup, stationList):
    distanceMatrix = [[99 for i in range(len(stationList))] for i in range(len(stationList))]
    for i in range(len(stationList)):
        distanceMatrix[i][i] = 0
    for fromStation in stationList:
        for toStation in stationGroup[fromStation]:
            distanceMatrix[stationList.index(fromStation)][stationList.index(toStation)] = 1
    return distanceMatrix

def countTeamLocation(stationList):
    f = open('CollegesLocation.xml', 'r')
    teamStationList = [0 for i in range(len(stationList))]
    while 1:
        line = f.readline().decode('utf-8')
        if not line:
            break
        for station in stationList:

            if line.find(station) >= 0 :
                stationNum = stationList.index(station)
                teamStationList[stationNum] = teamStationList[stationNum] + 1
    return teamStationList


def floydStations(stationGroup, stationList):
    distanceMatrix = initialDistanceMatrix(stationGroup, stationList)
    for k in range(len(stationList)):
        for i in range(len(stationList)):
            for j in range(len(stationList)):
                if (distanceMatrix[i][j] > distanceMatrix[i][k] + distanceMatrix[k][j]):
                    distanceMatrix[i][j] = distanceMatrix[i][k] + distanceMatrix[k][j]
    return distanceMatrix

def nearest3PointDis(shortestDistanceMatrix, i, j, k, startPoint):
    iToStartPoint = shortestDistanceMatrix[i][startPoint]
    jToStartPoint = shortestDistanceMatrix[j][startPoint]
    kToStartPoint = shortestDistanceMatrix[k][startPoint]
    if iToStartPoint <= jToStartPoint and iToStartPoint <= kToStartPoint:
        return iToStartPoint
    elif jToStartPoint <= kToStartPoint and jToStartPoint <= iToStartPoint:
        return jToStartPoint
    else:
        return kToStartPoint

def nearest2PointDis(shortestDistanceMatrix, i, j, startPoint):
    iToStartPoint = shortestDistanceMatrix[i][startPoint]
    jToStartPoint = shortestDistanceMatrix[j][startPoint]
    if iToStartPoint <= jToStartPoint:
        return iToStartPoint
    else:
        return jToStartPoint

def getPick3Point(stationList, teamLocation, shortestDistanceMatrix):
    shortestDistance = 9999
    iFinal = 9999
    jFinal = 9999
    kFinal = 9999
    for i in range(len(stationList)):
        for j in range(len(stationList)):
            for k in range(len(stationList)):
                if i != j and j != k and k != i:
                    temp = 0
                    for startPoint in range(len(stationList)):
                        if teamLocation[startPoint] > 0:
                            temp =temp + nearest3PointDis(shortestDistanceMatrix, i, j, k, startPoint) * teamLocation[startPoint]
                    if temp < shortestDistance:
                        shortestDistance = temp
                        iFinal = i
                        jFinal = j
                        kFinal = k
#    print iFinal, jFinal,kFinal
    return stationList[iFinal], stationList[jFinal], stationList[kFinal], shortestDistance

def getPick2Point(stationList, teamLocation, shortestDistanceMatrix):
    shortestDistance = 9999
    iFinal = 9999
    jFinal = 9999
    for i in range(len(stationList)):
        for j in range(len(stationList)):
            if i != j:
                temp = 0
                for startPoint in range(len(stationList)):
                    if teamLocation[startPoint] > 0:
                        temp =temp + nearest2PointDis(shortestDistanceMatrix, i, j, startPoint) * teamLocation[startPoint]
                if temp < shortestDistance:
                    shortestDistance = temp
                    iFinal = i
                    jFinal = j
#    print iFinal, jFinal
    return stationList[iFinal], stationList[jFinal], shortestDistance

def getPick1Point(stationList, teamLocation, shortestDistanceMatrix):
    shortestDistance = 9999
    iFinal = 9999
    for i in range(len(stationList)):
                temp = 0
                for startPoint in range(len(stationList)):
                    if teamLocation[startPoint] > 0:
                        temp = temp + shortestDistanceMatrix[startPoint][i] * teamLocation[startPoint]
                if temp < shortestDistance:
                    shortestDistance = temp
                    iFinal = i
#    print iFinal
    return stationList[iFinal], shortestDistance

if __name__=="__main__":

    stationGroup = getTheStationGraph()
    stationList = stationGroup.keys()
    teamLocation = countTeamLocation(stationList)
#    print teamLocation
    initialDistanceMatrix(stationGroup, stationList)
    shortestDistanceMatrix = floydStations(stationGroup, stationList)
    onePoint, oneShortestDistance = getPick1Point(stationList, teamLocation, shortestDistanceMatrix)
    print "\n", onePoint.encode("utf-8"), oneShortestDistance
    twoPoint1, twoPoint2, twoShortestDistance = getPick2Point(stationList, teamLocation, shortestDistanceMatrix)
    print "\n", twoPoint1.encode("utf-8"), twoPoint2.encode("utf-8"), twoShortestDistance
    threePoint1, threePoint2, threePoint3, threeShortestDistance = getPick3Point(stationList, teamLocation, shortestDistanceMatrix)
    print "\n", threePoint1.encode("utf-8"), threePoint2.encode("utf-8"), threePoint3, threeShortestDistance
