from controller import *
from ui import *

def main():
    controller = Controller()
    ui = UI(controller)
    ui.run()


main()