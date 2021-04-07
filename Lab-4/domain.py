from constants import *
import pickle
import numpy as np

class Sensor:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__areas = [] # the list that stores how many cells can be seen with an energy level i
        self.__currentEnergyLevel = 0


    def getX(self):
        return self.__x


    def getY(self):
        return self.__y


    def getEnergyLevel(self):
        return self.__currentEnergyLevel


    def computeMaximumFeasibleArea(self, map):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        numberOfCellsSurveilled = 0 
        
        for energyLevel in range(1, 6):
            for direction in directions:
                possibleCoveredAreaX = self.__x + energyLevel*direction[0]
                possibleCoveredAreaY = self.__y + energyLevel*direction[1]

                if map.isTheCellAWall(possibleCoveredAreaX, possibleCoveredAreaY) or not isPositionWithinBoundaries(possibleCoveredAreaX, possibleCoveredAreaY):
                    positionToBeDeleted = directions.index(direction)
                    del directions[positionToBeDeleted]
                else:
                    numberOfCellsSurveilled += 1             
            
            self.__areas.append(numberOfCellsSurveilled)


    def getSurveillanceAreaByEnergyLevel(self, energyLevel):
        if not self.__areas: 
            raise Exception("The maximum feasible area for each energy level has not yet been computed.")
        return self.__areas[energyLevel]


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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