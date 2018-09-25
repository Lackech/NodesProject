class Interface:

    # Interface's constructor
    def __init__(self):
        self.panel = Tk()

    def showMessage(self,message):
        print(message)

    def getInput(self,message):
        input(message)