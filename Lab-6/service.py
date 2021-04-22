from random import randint
import numpy as np

class KMeansService:
    def __init__(self, repository):
        self.__repository = repository

    def pickTheInitialCentroidsRandomly(self, numberOfCentroidsK):
        centroidsAsPoints = []
        points = self.__repository.getTheUnlabelledPoints()

        for centroidIndex in range(0, numberOfCentroidsK):
            pointIndex = randint(0, len(points) - 1)
            point = self.__repository.getUnlabelledPointByIndex(pointIndex)
            while point in centroidsAsPoints:
                pointIndex = randint(0, len(points) - 1)
                point = self.__repository.getUnlabelledPointByIndex(pointIndex)
            centroidsAsPoints.append(point)

        centroids = list(map(lambda x: Centroid(x.getX(), y.getY()), centroidsAsPoints))
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

        meanOfTheXCoordinates = np.average(list(filter(lambda x: x.getX(), pointsInTheCluster))) 
        meanOfTheYCoordinates = np.average(list(filter(lambda y: y.getY(), pointsInTheCluster))) 

        return (meanOfTheXCoordinates, meanOfTheYCoordinates)


    def repositionCentroids(self):
        centroids = self.__repository.getCentroids()

        for centroid in centroids:
            newPositionOfTheCentroid = self.computeTheMeanOfACluster(centroid.getId())
            centroid.setX()