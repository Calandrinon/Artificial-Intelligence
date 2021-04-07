from repository import *
from controller import *
from ui import *

def main():
    repository = Repository()
    controller = Controller(repository)
    ui = UI(controller)
    ui.run()


main()