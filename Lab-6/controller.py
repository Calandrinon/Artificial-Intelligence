
class KMeansController:

    def __init__(self, service):
        self.__service = service


    def pickTheInitialCentroidsRandomly(self, numberOfDesiredClustersK):
        self.__service.pickTheInitialCentroidsRandomly(numberOfDesiredClustersK)


    def runAnIteration(self):
        self.__service.computeTheDistancesFromThePointsToTheCentroids()
        self.__service.repositionCentroids()

        return self.__service.getCentroids()
