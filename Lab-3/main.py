from gui import *
from ui import *
from controller import *
from repository import *
from domain import *

def main():
    numberOfGenerations = 20
    selectedIndividualsFromAGeneration = 10
    startingPosition = (4, 7)
    populationSize = 20
    individualSize = 10 # 10 is the length of the longest path the drone can take

    repository = Repository()
    repository.createPopulation([startingPosition[0], startingPosition[1], populationSize, individualSize])
    controller = Controller(repository)
    ui = UI(controller)
    
    finalStatistics = ui.solver([numberOfGenerations, selectedIndividualsFromAGeneration, startingPosition[0], startingPosition[1], populationSize, individualSize])
    print("Average & standard deviation: {}".format(finalStatistics))


main()