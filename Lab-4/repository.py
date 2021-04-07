from domain import *
import json

class Repository:
    def __init__(self):
        self.__map = Map()
        self.__sensors = []
        self.readConfigFile("parameters.json")


    def readConfigFile(self, configFile):
        with open(configFile) as jsonFile:
            data = json.load(jsonFile)
            self.createDrone(data["dronePosition"], data["droneEnergy"])
            self.__sensors = [Sensor(position[0], position[1]) for position in data["sensors"]]
            self.__map.loadMap(data["mapFile"])
            print(data)


    def createDrone(self, positionAsList, energy):
        self.__drone = Drone(*positionAsList)


    def getSensors(self):
        return self.__sensors


    def getMap(self):
        return self.__map