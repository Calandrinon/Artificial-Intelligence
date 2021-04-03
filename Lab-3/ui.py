from gui import *
from random import randint

class UI:
    def __init__(self, controller):
        self.__controller = controller
        self.__running = True
        self.__modifiedMap = False
        self.__gui = GUI(self.__controller)
        self.__quit = False


    def __getGenerations(self):
        generations = int(input("Enter the number of generations:"))
        return generations


    def __getPopulations(self):
        populations = int(input("Enter the number of populations:"))
        return populations

    def __getNumberOfSelectedIndividuals(self):
        selectedIndividuals = int(input("Enter the number of selected individuals: "))
        return selectedIndividuals


    def __getStartingPosition(self):
        startX = int(input("Enter the X coordinate of the starting position:"))
        startY = int(input("Enter the Y coordinate of the starting position:"))
        return (startX, startY)


    def __getPopulationSize(self):
        size = int(input("Enter the population size:"))
        return size 


    def __getIndividualSize(self):
        size = int(input("Enter the individual size:"))
        return size


    def __printMapOptions(self):
        options = """        1. Create a random map
        2. Load a map
        3. Save the current map
        4. Visualize the map
        5. Run
        0. Exit
        """
        print(options)

    
    def __getMapOptions(self):
        self.__printMapOptions()
        option = int(input("Enter an option: "))

        while option < 0 or option > 5:
            option = int(input("Enter an option between 0 and 5: "))

        if option == 0:
            self.__quit = True
            return

        if option == 1:
            self.__controller.createRandomMap()
            self.__modifiedMap = True
        elif option == 2:
            fileName = input("Enter the filename: ")
            self.__controller.loadMap(fileName)
            self.__modifiedMap = True
        elif option == 3:
            fileName = input("Enter the filename: ")
            self.__controller.saveMap(fileName)
            self.__modifiedMap = True
        elif option == 4:
            self.__gui.visualizeMap()
            self.__modifiedMap = True
        else:
            self.__modifiedMap = False


    def __startSolver(self):
        numberOfGenerations = self.__getGenerations() 
        numberOfPopulations = self.__getPopulations()
        selectedIndividualsFromAGeneration = 100 #self.__getNumberOfSelectedIndividuals()
        startingPosition = self.__getStartingPosition() 
        populationSize = self.__getPopulationSize()
        individualSize = self.__getIndividualSize()

        randomSeeds = [randint(0, 100000) for i in range(0, numberOfPopulations)]
        for populationIndex in range(0, numberOfPopulations):
            print("Seed for population {}: {}".format(populationIndex, randomSeeds[populationIndex]))
            self.__controller.createPopulation(startingPosition[0], startingPosition[1], populationSize, individualSize)

        self.__controller.mergeAllPopulations()

        finalStatistics = self.__gui.solver([numberOfGenerations, numberOfPopulations, selectedIndividualsFromAGeneration, startingPosition[0], startingPosition[1], populationSize, individualSize])

        print("Average & standard deviation of all generations: {}".format(finalStatistics))


    def run(self):
        self.__running = True
        self.__controller.resetRepository()

        while self.__running:
            self.__modifiedMap = False
            self.__getMapOptions() 
            if self.__quit == True:
                print("Bye.")
                return

            if not self.__modifiedMap:
                self.__startSolver()
