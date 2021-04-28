import math

class Point:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__expectedCluster = None
        self.__datasetLabel = None
        self.__predictedLabel = None


    def getX(self):
        return self.__x


    def getY(self):
        return self.__y


    def getTheExpectedCluster(self):
        return self.__expectedCluster


    def getTheDatasetLabel(self):
        return self.__datasetLabel


    def getThePredictedLabel(self):
        return self.__predictedLabel


    def setX(self, x):
        self.__x = x


    def setY(self, y):
        self.__y = y


    def setTheExpectedCluster(self, expectedCluster):
        self.__expectedCluster = expectedCluster


    def setTheDatasetLabel(self, datasetLabel):
        self.__datasetLabel = datasetLabel


    def setThePredictedLabel(self, predictedLabel):
        self.__predictedLabel = predictedLabel

    
    def distanceToAnotherPoint(self, anotherPoint):
        return math.sqrt((self.getX() - anotherPoint.getX())**2 + (self.getY() - anotherPoint.getY())**2)         


    def __repr__(self):
        return str((self.__x, self.__y, self.__expectedCluster, self.__datasetLabel, self.__predictedLabel))  


class Centroid:
    id = -1

    def __init__(self, x, y):
        self.__x = x 
        self.__y = y 
        self.__previousPosition = None
        Centroid.id += 1
        self.__id = Centroid.id
        self.__label = chr(ord('A')+self.__id)
        self.__clusterColors = []


    def distanceToAPoint(self, point):
        pointOfTheCentroid = Point(self.__x, self.__y)
        return pointOfTheCentroid.distanceToAnotherPoint(point)

    
    def getLabel(self):
        return self.__label


    def setLabel(self, label):
        self.__label = label
        

    def getId(self):
        return self.__id


    def setId(self, id):
        self.__id = id

    
    def setX(self, x):
        self.__x = x


    def setY(self, y):
        self.__y = y


    def setPosition(self, x, y):
        self.__previousPosition = (self.__x, self.__y)
        self.setX(x)
        self.setY(y)


    def getX(self):
        return self.__x


    def getY(self):
        return self.__y

    
    def getTheCurrentPosition(self):
        return (self.__x, self.__y)


    def getThePreviousPosition(self):
        return self.__previousPosition


    def __repr__(self):
        return str((self.getX(), self.getY(), self.__id))