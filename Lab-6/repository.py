import csv
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
            for row in reader:
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
        self.__centroids = centroids


    def getUnlabelledPointByIndex(self, index):
        try:
            return self.__unlabelledPoints[index] 
        except Exception as e:
            raise e