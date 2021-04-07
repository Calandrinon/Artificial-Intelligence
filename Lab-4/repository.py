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
            self.__sensors = data["sensors"]
            self.__map.loadMap(data["mapFile"])
            print(data)


    def createDrone(self, positionAsList, energy):
        self.__drone = Drone(*positionAsList)