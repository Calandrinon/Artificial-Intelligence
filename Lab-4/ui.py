from constants import *
import pygame
import matplotlib.pyplot as plt


class UI:
    def __init__(self, controller):
        self.__controller = controller


    def initialisePygame(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Drone colony optimization")
        
        self.__screen = pygame.display.set_mode((400,400))
        self.__screen.fill(WHITE)
        pygame.display.flip()
        return self.__screen


    def closePygameOnEvent(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closePygame()
                    running = False


    def closePygame(self):
        pygame.quit()


    def createImage(self, map, colour = BLUE, background = WHITE):
        image = pygame.Surface((map.n * MAP_SIZE, map.m * MAP_SIZE))
        brick = pygame.Surface((20,20))
        brick.fill(colour)
        image.fill(background)
        for i in range(map.n):
            for j in range(map.m):
                if (map.getSurface()[i][j] == 1):
                    image.blit(brick, (j * MAP_SIZE, i * MAP_SIZE))
                    
        return image


    def displayMap(self):
        map = self.__controller.getMap()
        self.initialisePygame()
        self.__screen.blit(self.createImage(map), (0,0))
        pygame.display.flip()


    def displayMaximumSurveillanceAreaOfASensor(self, sensor):
        coveredAreaTexture = pygame.Surface((20,20))
        coveredAreaTexture.fill(LIGHT_BLUE) 
        sensor.computeMaximumFeasibleArea(self.__controller.getMap())

        for energyLevel in range(0, sensor.getMaximumUsefulEnergyLevel()):
            surveillanceArea = sensor.getSurveillanceAreaByEnergyLevel(energyLevel, self.__controller.getMap())
            for position in surveillanceArea:
                self.__screen.blit(coveredAreaTexture, (position[1]*MAP_SIZE, position[0]*MAP_SIZE))
        
        print("Maximum level of useful energy for the sensor on position {}: {}".format(sensor.getPosition(), sensor.getMaximumUsefulEnergyLevel()))


    def displaySensors(self):
        sensors = self.__controller.getSensors()
        sensorTexture = pygame.Surface((20,20))
        sensorTexture.fill(BLACK)

        for sensor in sensors:
            sensorPosition = sensor.getPosition()
            self.__screen.blit(sensorTexture, (sensorPosition[1]*MAP_SIZE, sensorPosition[0]*MAP_SIZE))
            self.displayMaximumSurveillanceAreaOfASensor(sensor)
            pygame.display.flip()

        self.printDistancesBetweenSensors()


    def printDistancesBetweenSensors(self):
        self.__controller.computeDistancesBetweenPairsOfSensors()
        sensors = self.__controller.getSensors()

        for sensor in sensors:
            print("Distances to other sensors for the sensor {} on position {}: {}".format(sensor.getId(), sensor.getPosition(), sensor.getDistancesToOtherSensors()))


    def printDummyGraph(self):
        print("Sensor graph:")
        print(self.__controller.getGraph())


    def displayGraph(self):
        x_axis, y_axis = self.__controller.getIterationIndexesAndPathLengths()
        plt.xlabel("Iteration")
        plt.ylabel("Path length")
        plt.plot(x_axis, y_axis, color="green")
        plt.legend(["Average path length"], labelcolor=["green"])
        #plt.pause(0.05)
        plt.show()


    def startIterations(self):
        self.__controller.runMultipleIterations()


    def run(self):
        self.displayMap()
        self.displaySensors()
        self.printDummyGraph()
        self.startIterations()
        print("Done.")
        self.displayGraph()
        self.closePygameOnEvent()    