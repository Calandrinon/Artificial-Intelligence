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


    def runEdgeSelectionAndPheromoneUpdate(self):
        drones = self.__repository.getDrones()

        for drone in drones:
            drone.startEdgeSelection()
        
        self.__repository.getGraph().updatePheromoneLevels(drones)
        
    
    def runMultipleIterations(self):
        numberOfIterations = self.__repository.getNumberOfIterations()
        for iterationIndex in range(0, numberOfIterations):
            print("--------------------------------------- Iteration {} ---------------------------------------".format(iterationIndex))
            self.runEdgeSelectionAndPheromoneUpdate()


    def getGraph(self):
        return self.__repository.getGraph()


    def getDrone(self):
        return self.__repository.getDrone()