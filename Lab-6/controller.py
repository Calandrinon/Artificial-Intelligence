
class KMeansController:

    def __init__(self, service):
        self.__service = service


    def pickTheInitialCentroidsRandomly(self, numberOfDesiredClustersK):
        self.__service.pickTheInitialCentroidsRandomly(numberOfDesiredClustersK)


    def runAnIteration(self):
        self.__service.computeTheDistancesFromThePointsToTheCentroids()
        self.__service.repositionCentroids()

        return self.__service.getCentroids()


    def getThePoints(self):
        return self.__service.getThePoints()


    def didTheModelConverge(self):
        return self.__service.didTheModelConverge()

    
    def generateColors(self, k):
        return self.__service.generateColors(k)

    
    def getClusterColors(self):
        return self.__service.getClusterColors()