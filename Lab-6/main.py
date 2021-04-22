from repository import Repository
from service import KMeansService
from controller import KMeansController
from ui import UI


def main():
    repository = Repository()
    service = KMeansService(repository)
    controller = KMeansController(service)
    ui = UI(controller)

    k = int(input("Choose the number of clusters K: "))

    ui.runTheAlgorithm(k)

main()