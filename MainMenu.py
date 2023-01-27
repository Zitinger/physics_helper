import sys
from Calculator import Calculator
from Graph import Graph
from References import References
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.graph = Graph()
        self.references = References()
        uic.loadUi('uis/main_menu.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Главное меню')
        self.move(100, 400)
        self.calculatorBtn.clicked.connect(self.calculator.show)
        self.graphBtn.clicked.connect(self.graph.show)
        self.referencesBtn.clicked.connect(self.references.show)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())
