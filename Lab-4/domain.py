from constants import *
import pickle
import numpy as np
import copy
import random

class Sensor:
    total = -1

    def __init__(self, x, y):
        Sensor.total += 1
        self.__x = x
        self.__y = y
        self.__areas = [] # the list that stores how many cells can be seen with an energy level i
        self.__currentEnergyLevel = 0
        self.__distancesToOtherSensors = {}
        self.__id = Sensor.total


    def getId(self):
        return self.__id


    def getPosition(self):
        return (self.__x, self.__y)


    def getMaximumUsefulEnergyLevel(self):
        return len(self.__areas)


    def getEnergyLevel(self):
        return self.__currentEnergyLevel

    
    def getDistancesToOtherSensors(self):
        return self.__distancesToOtherSensors


    def computeMaximumFeasibleArea(self, map):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for energyLevel in range(1, 6):
            energyLevelAreas = []

            for direction in directions:
                possibleCoveredAreaX = self.__x + energyLevel*direction[0]
                possibleCoveredAreaY = self.__y + energyLevel*direction[1]

                if map.isTheCellAWall(possibleCoveredAreaX, possibleCoveredAreaY):
                    positionToBeDeleted = directions.index(direction)
                    directions[positionToBeDeleted] = 0
                else:
                    energyLevelAreas.append((possibleCoveredAreaX, possibleCoveredAreaY))

            directions = list(filter(lambda x: x != 0, directions))
            self.__areas.append(energyLevelAreas)

        self.__areas = list(filter(lambda x: x != [], self.__areas))


    def getSurveillanceAreaByEnergyLevel(self, energyLevel, map):
        if not self.__areas: 
            self.computeMaximumFeasibleArea(map)

        areas = []
        for level in range(1, energyLevel+1):
            areas.append(self.__areas[level])
        return self.__areas[energyLevel]


    def breadthFirstSearch(self, map, allSensors):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = [(self.__x, self.__y)]
        distances = [[0 for j in range(0, map.m)] for i in range(0, map.n)]
        visited = [[0 for j in range(0, map.m)] for i in range(0, map.n)]

        while queue:
            currentX, currentY = queue.pop(0)
            visited[currentX][currentY] = 1

            for direction in directions:
                nextX = currentX + direction[0]
                nextY = currentY + direction[1]

                if not map.isTheCellAWall(nextX, nextY) and visited[nextX][nextY] == 0:
                    queue.append((nextX, nextY))
                    distances[nextX][nextY] = distances[currentX][currentY] + 1

        for sensor in allSensors:
            position = sensor.getPosition()
            self.__distancesToOtherSensors[sensor.getId()] = distances[position[0]][position[1]] - 1 if position != self.getPosition() else 0


    def __repr__(self):
        return "|Sensor {} at position {}|".format(self.getId(), self.getPosition())


class SensorGraph:
    def __init__(self, sensors):
        self.__sensors = sensors
        self.__costMatrix = [sensor.getDistancesToOtherSensors() for sensor in sensors]
        self.__pheromoneMatrix = [[0.01 for i in range(0, len(self.__sensors))] for sensor in sensors]


    def getEdgeCost(self, indexOfSensorI, indexOfSensorJ):
        return self.__costMatrix[indexOfSensorI][indexOfSensorJ]


    def getSensors(self):
        return self.__sensors


    def getNumberOfSensors(self):
        return len(self.__sensors)


    def eta(self, indexOfSensorI, indexOfSensorJ, beta):
        return (1 / self.__costMatrix[indexOfSensorI][indexOfSensorJ])**beta


    def tau(self, indexOfSensorI, indexOfSensorJ, alpha):
        return self.__pheromoneMatrix[indexOfSensorI][indexOfSensorJ]**alpha


    def __repr__(self):
        stringRepresentation = "Cost matrix:\n"
        for line in self.__costMatrix:
            stringRepresentation += str(line) + "\n"
        stringRepresentation += "Pheromone matrix:\n"    
        for line in self.__pheromoneMatrix:
            stringRepresentation += str(line) + "\n"

        return stringRepresentation


    def __applyPheromoneEvaporation(self, rho = 0.95):
        for i in range(0, len(self.__sensors)):
            for j in range(0, i):
                self.__pheromoneMatrix[i][j] *= (1 - rho)
        """
        This old version would most likely apply evaporation on each edge twice, because
        the graph is a symmetric matrix.

        for sensorI in self.__sensors:
            for sensorJ in self.__sensors:
                self.__pheromoneMatrix[sensorI.getId()][sensorJ.getId()] *= (1-rho)
        """


    def __updatePheromoneOnTheEdge(self, drone, sensorI, sensorJ):
        sensorI = sensorI.getId()
        sensorJ = sensorJ.getId()
        deltaTau = 1 / drone.getPathCost()
        self.__pheromoneMatrix[sensorI][sensorJ] += deltaTau


    def updatePheromoneLevels(self, drones):
        self.__applyPheromoneEvaporation()
        for drone in drones:
            path = drone.getPath()
            for index in range(0, len(path)-1):
                self.__updatePheromoneOnTheEdge(drone, path[index], path[index+1])
            self.__updatePheromoneOnTheEdge(drone, path[-1], path[0])


class Drone:
    total = -1

    def __init__(self, x, y):
        Drone.total += 1
        self.x = x
        self.y = y
        self.__id = Drone.total


    def getId(self):
        return self.__id


    def setGraph(self, graph):
        self.__graph = graph
        self.__visitedSensors = {}
        self.__path = []
        self.__totalPathCost = 0

        for node in graph.getSensors():
            self.__visitedSensors[node.getId()] = False

        print("Visited sensors list: {}".format(self.__visitedSensors))

    
    def resetGraph(self):
        self.setGraph(self.__graph) 


    def getPath(self):
        return self.__path


    def getPathCost(self):
        return self.__totalPathCost


    def getGraph(self):
        return self.__graph


    def setPosition(self, x, y):
        self.x = x
        self.y = y


    def setEnergy(self, energy):
        self.__energy = energy


    def getEnergy(self):
        return self.__energy


    def getPosition(self):
        return (self.x, self.y)

                  
    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))
        
        return mapImage


    def computeTheDesirabilityOfTheNeighbourNodes(self, currentNode):
        feasibleExpansions = []

        for sensor in self.__getUnmarkedSensors():
            if currentNode.getId() != sensor.getId():
                tauAndEtaProductNumerator = self.__graph.tau(currentNode.getId(), sensor.getId(), 1) * self.__graph.eta(currentNode.getId(), sensor.getId(), 1)
                feasibleExpansions.append((tauAndEtaProductNumerator, sensor))

        productDenominator = sum([nodeDesirability[0] for nodeDesirability in feasibleExpansions])
        print("productDenominator: {}".format(productDenominator))
        desirabilityOfTheNeighbourNodes = list(map(lambda x: (x[0] / productDenominator, x[1]), feasibleExpansions))

        return desirabilityOfTheNeighbourNodes


    def __getMarkedSensors(self):
        return list(filter(lambda x: self.__visitedSensors[x.getId()] == True, self.__graph.getSensors()))


    def __getUnmarkedSensors(self):
        return list(filter(lambda x: self.__visitedSensors[x.getId()] == False, self.__graph.getSensors()))
            

    def startEdgeSelection(self):
        self.resetGraph()
        currentSensorNode = list(filter(lambda x: x.getPosition() == (self.x, self.y), self.__graph.getSensors()))[0]
        sensorIndex = currentSensorNode.getId()
        print("------------------------------------------------------------------------------------------------------------------")
        print("The drone {} is near the sensor {} at position {}.".format(self.__id, sensorIndex, currentSensorNode.getPosition()))
        self.__path.append(currentSensorNode)
        
        while len(self.__path) != len(self.__graph.getSensors()):
            if self.__visitedSensors[sensorIndex] == False: # check if the node was visited
                self.__visitedSensors[sensorIndex] = True
                desirabilityOfTheNeighbourNodes = self.computeTheDesirabilityOfTheNeighbourNodes(currentSensorNode)
                desirabilityOfTheNeighbourNodes.sort(key=lambda x: x[0]) # the second element of each tuple is the sensor, whereas the first element is the desirability
                print("desirabilityOfTheNeighbourNodes: {}".format(desirabilityOfTheNeighbourNodes))

                randomChance = random.random()
                cumulativeSum = 0

                for nodeDesirability in desirabilityOfTheNeighbourNodes:
                    cumulativeSum += nodeDesirability[0]
                    if randomChance <= cumulativeSum:
                        self.__totalPathCost += self.__graph.getEdgeCost(currentSensorNode.getId(), nodeDesirability[1].getId())
                        currentSensorNode = nodeDesirability[1]
                        sensorIndex = currentSensorNode.getId()
                        self.__path.append(currentSensorNode)
                        break
                
                print("Added node {} to path: {}".format(sensorIndex, self.__path))
        self.__totalPathCost += self.__graph.getEdgeCost(self.__path[0].getId(), self.__path[-1].getId())
        print("Drone's path: {}".format(self.__path))
        print("Path cost: {}".format(self.__totalPathCost))


class Map:
    def __init__(self, n = MAP_SIZE, m = MAP_SIZE):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    
    def getSurface(self):
        return self.surface


    def setSurface(self, surface):
        self.surface = surface


    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1


    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()


    def isPositionWithinBoundaries(self, x, y):
        return x >= 0 and x < self.n and y >= 0 and y < self.m


    def isTheCellAWall(self, x, y):
        if not self.isPositionWithinBoundaries(x, y):
            return True 
        return self.surface[x][y] == 1
        

    def image(self, colour = BLUE, background = WHITE):
        mapImage = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        mapImage.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    mapImage.blit(brick, ( j * 20, i * 20))
                
        return mapImage

                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string