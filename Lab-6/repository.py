import csv, copy
from domain import Point

class Repository:

    def __init__(self):
        self.__labelledPoints = []
        self.__unlabelledPoints = []
        self.readTheDataset('dataset.csv')
        self.__centroids = []


    def readTheDataset(self, filename): 
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            rows = []

            for row in reader:
                rows.append(row)
            del rows[0]

            for row in rows:
                row[1], row[2] = float(row[1]), float(row[2])
                labelledPoint = Point(*row[1:3])
                labelledPoint.setTheExpectedCluster(row[0])
                self.__labelledPoints.append(labelledPoint)
                unlabelledPoint = Point(*row[1:3])
                self.__unlabelledPoints.append(unlabelledPoint)


    def getTheLabelledPoints(self):
        return self.__labelledPoints


    def getTheUnlabelledPoints(self):
        return self.__unlabelledPoints


    def getCentroids(self):
        return self.__centroids


    def setCentroids(self, centroids):
        self.__centroids = copy.deepcopy(centroids)


    def getUnlabelledPointByIndex(self, index):
        try:
            return self.__unlabelledPoints[index] 
        except Exception as e:
            raise e

    
    def setClusterColors(self, colors):
        self.__clusterColors = colors


    def getClusterColors(self):
        return self.__clusterColors