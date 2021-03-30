from gui import *
from ui import *
from controller import *
from repository import *
from domain import *

def main():
    repository = Repository()
    controller = Controller(repository)
    ui = UI(controller)
    ui.run()


main()