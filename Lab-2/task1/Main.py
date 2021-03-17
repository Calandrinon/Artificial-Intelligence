from Domain import *
from Repository import Repository
from Controller import Controller
from UI import UI


def main():
    repository = Repository()
    controller = Controller(repository)
    ui = UI(controller)
    ui.run()
    

if __name__ == "__main__":
    main()