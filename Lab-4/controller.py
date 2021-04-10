class Controller:
    def __init__(self, repository):
        self.__repository = repository


    def getSensors(self):
        return self.__repository.getSensors()


    def getMap(self):
        return self.__repository.getMap()


    def computeDistancesBetweenPairsOfSensors(self):
        sensors = self.__repository.getSensors() 
        map = self.__repository.getMap()
        
        for sensor in sensors:
            sensor.breadthFirstSearch(map, sensors)

        return sensor.getDistancesToOtherSensors()


    def getGraph(self):
        return self.__repository.getGraph()