import math

class Point:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__expectedCluster = None


    def getX(self):
        return self.__x


    def getY(self):
        return self.__y


    def getTheExpectedCluster(self):
        return self.__expectedCluster


    def setX(self, x):
        self.__x = x


    def setY(self, y):
        self.__y = y


    def setTheExpectedCluster(self, expectedCluster):
        self.__expectedCluster = expectedCluster

    
    def distanceToAnotherPoint(self, anotherPoint):
        return math.sqrt((self.getX() - anotherPoint.getX())**2 + (self.getY() - anotherPoint.getY())**2)         


    def __repr__(self):
        return str((self.__x, self.__y, self.__expectedCluster))  


class Centroid:
    id = -1

    def __init__(self, x, y):
        self.__x = x 
        self.__y = y 
        self.__previousPosition = None
        Centroid.id += 1
        self.__id = Centroid.id


    def distanceToAPoint(self, point):
        pointOfTheCentroid = Point(self.__x, self.__y)
        return pointOfTheCentroid.distanceToAnotherPoint(point)
        

    def getId(self):
        return self.__id

    
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