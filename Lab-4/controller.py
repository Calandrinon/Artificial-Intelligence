class Controller:
    def __init__(self, repository):
        self.__repository = repository


    def getSensors(self):
        return self.__repository.getSensors()


    def getMap(self):
        return self.__repository.getMap()