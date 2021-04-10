from domain import *
import json

class Repository:
    def __init__(self):
        self.__map = Map()
        self.__sensors = []
        self.__drones = []
        self.readConfigFile("parameters.json")


    def readConfigFile(self, configFile):
        with open(configFile) as jsonFile:
            data = json.load(jsonFile)
            self.__alpha, self.__beta, self.__rho = data["alpha"], data["beta"], data["rho"]
            self.__sensors = [Sensor(position[0], position[1]) for position in data["sensors"]]
            self.__sensorGraph = SensorGraph(self.__sensors)
            self.__map.loadMap(data["mapFile"])
            self.__numberOfIterations = data["numberOfIterations"]
            self.createDrones(data["dronePosition"], data["numberOfDrones"], data["droneEnergy"])
            print(data)


    def createDrone(self, positionAsList, energy):
        self.__drone = Drone(*positionAsList)
        self.__drone.setEnergy(energy)
        self.__drone.setGraph(self.__sensorGraph)
        self.__drones.append(self.__drone)


    def createDrones(self, positionAsList, numberOfDrones, energy):
        for index in range(0, numberOfDrones):
            self.createDrone(positionAsList, energy)


    def getDrone(self):
        return self.__drone


    def getDrones(self):
        return self.__drones


    def getSensors(self):
        return self.__sensors


    def getGraph(self):
        return self.__sensorGraph

    
    def getNumberOfIterations(self):
        return self.__numberOfIterations


    def getAlphaBetaAndRho(self):
        return (self.__alpha, self.__beta, self.__rho)


    def getMap(self):
        return self.__map