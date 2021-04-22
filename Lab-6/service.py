from random import randint, random
import numpy as np
import colorsys
from domain import Centroid

class KMeansService:
    def __init__(self, repository):
        self.__repository = repository

    def pickTheInitialCentroidsRandomly(self, numberOfCentroidsK):
        centroids = []
        points = self.__repository.getTheUnlabelledPoints()

        for centroidIndex in range(0, numberOfCentroidsK):
            pointIndex = randint(0, len(points) - 1)
            point = self.__repository.getUnlabelledPointByIndex(pointIndex)

            while point in centroids:
                pointIndex = randint(0, len(points) - 1)
                point = self.__repository.getUnlabelledPointByIndex(pointIndex)

            centroid = Centroid(point.getX(), point.getY())
            centroids.append(centroid)

        self.__repository.setCentroids(centroids)
        return centroids
    

    def computeTheDistancesFromThePointsToTheCentroids(self):
        points = self.__repository.getTheUnlabelledPoints()
        centroids = self.__repository.getCentroids()

        for point in points:
            distancesToTheCentroids = []
            for centroid in centroids:
                distanceToCentroid = centroid.distanceToAPoint(point)
                distancesToTheCentroids.append((centroid, distanceToCentroid))
            
            closestCentroid = min(distancesToTheCentroids, key=lambda x: x[1])[0]
            point.setTheExpectedCluster(closestCentroid.getId())

    
    def computeTheMeanOfACluster(self, clusterId):
        points = self.__repository.getTheUnlabelledPoints()
        pointsInTheCluster = list(filter(lambda x: x.getTheExpectedCluster() == clusterId, points))

        meanOfTheXCoordinates = np.average(list(map(lambda x: x.getX(), pointsInTheCluster))) 
        meanOfTheYCoordinates = np.average(list(map(lambda y: y.getY(), pointsInTheCluster))) 

        return (meanOfTheXCoordinates, meanOfTheYCoordinates)


    def repositionCentroids(self):
        centroids = self.__repository.getCentroids()

        for centroid in centroids:
            newPositionOfTheCentroid = self.computeTheMeanOfACluster(centroid.getId())
            centroid.setPosition(newPositionOfTheCentroid[0], newPositionOfTheCentroid[1])

        return centroids


    def getCentroids(self):
        return self.__repository.getCentroids()


    def getTheUnlabelledPoints(self):
        return self.__repository.getTheUnlabelledPoints()    

    
    def didTheModelConverge(self):
        centroids = self.__repository.getCentroids()
        converged = True

        for centroid in centroids:
            positionDifference = np.array(centroid.getThePreviousPosition()) - np.array(centroid.getTheCurrentPosition())
            print("positionDifference: {}".format(positionDifference))
            if positionDifference[0] != 0 or positionDifference[1] != 0:
                converged = False

        return converged


    def generateColors(self, k):
        rgbColorsAsFloats = [(random(), random(), random()) for i in range(0, k)]
        self.__repository.setClusterColors(rgbColorsAsFloats)

    
    def getClusterColors(self):
        return self.__repository.getClusterColors()
