import csv, copy
from domain import Point

class Repository:

    def __init__(self):
        self.__points = []
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
                point = Point(*row[1:3])
                point.setTheDatasetLabel(row[0])
                self.__points.append(point)


    def getThePoints(self):
        return self.__points


    def setThePoints(self, points):
        self.__points = points


    def getCentroids(self):
        return self.__centroids


    def setCentroids(self, centroids):
        self.__centroids = copy.deepcopy(centroids)


    def getPointByIndex(self, index):
        try:
            return self.__points[index] 
        except Exception as e:
            raise e

    
    def setClusterColors(self, colors):
        self.__clusterColors = colors


    def getClusterColors(self):
        return self.__clusterColors