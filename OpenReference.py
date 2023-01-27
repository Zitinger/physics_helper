import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QStatusBar, QPlainTextEdit


class OpenReference(QWidget):
    def __init__(self, name, description, type):
        super().__init__()
        uic.loadUi('uis/open_reference.ui', self)
        self.name, self.description, self.type = name, description, type
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Просмотр записи')
        self.type_txt.setText(self.type)
        self.name_textEdit.setFontPointSize(18)
        self.name_textEdit.setPlainText(self.name.capitalize())
        self.description_textEdit.setFontPointSize(16)
        if self.type == "Формула":
            self.description_textEdit.setPlainText(self.description)
        else:
            self.description_textEdit.setPlainText(self.description.capitalize())
