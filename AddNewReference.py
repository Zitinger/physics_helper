import sqlite3
import time
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QStatusBar, QPlainTextEdit


class AddNewReference(QWidget):
    def __init__(self, references_widget):
        super().__init__()
        uic.loadUi('uis/add_new_reference.ui', self)
        self.references = sqlite3.connect("references.sqlite")
        self.cur = self.references.cursor()
        self.parent = references_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить новую запись')

        self.description_label.setAutoFillBackground(True)

        self.buttonBox.accepted.connect(self.add_reference)
        self.buttonBox.rejected.connect(self.close)
        self.type_comboBox.currentIndexChanged.connect(self.comboBox_changed)
        self.type_comboBox.currentIndexChanged.connect(self.comboBox_changed)

    def comboBox_changed(self):
        if self.type_comboBox.currentText() == 'Формула':
            self.quantity_txt.setEnabled(True)
            self.quantity_lineEdit.setEnabled(True)
        else:
            self.quantity_txt.setEnabled(False)
            self.quantity_lineEdit.setText('')
            self.quantity_lineEdit.setEnabled(False)

    def add_reference(self):
        quantity = None
        if self.type_comboBox.currentText() == 'Формула':
            quantity = self.quantity_lineEdit.text().lower()
        if self.name_textEdit.toPlainText() and self.description_textEdit.toPlainText() \
                and self.type_comboBox.currentText():
            name, description, type = (s.lower().rstrip().lstrip() for s in [self.name_textEdit.toPlainText(),
                                                                             self.description_textEdit.toPlainText(),
                                                                             self.type_comboBox.currentText()])

            symbols_ok = ' abcdefghijklmnopqrstuvwxyz+-/*^.()=0123456789'
            all_symbols_is_right = False
            if len(description) > 4:
                if description[2] == '=' and description[1] == ' ' and description[3] == ' ' or \
                        description[3] == '=' and description[2] == ' ' and description[4] == ' ':
                    all_symbols_is_right = True

            for symb in description:
                if symb not in symbols_ok:
                    all_symbols_is_right = False

            replace = [('+', ' + '), ('-', ' - '), ('*', ' * '), ('/', ' / '), ('=', ' = '), ('^', ' ^ '), ('(', ' ( '),
                       (')', ' ) ')]
            description_checking = description
            for pair in replace:
                description_checking = description_checking.replace(pair[0], pair[1])
            for symb in description_checking.split():
                if len(symb) > 2:
                    all_symbols_is_right = False

            if description.count('(') == description.count(')') and description.count(
                    '=') == 1 and all_symbols_is_right:
                self.cur.execute(f"INSERT INTO references_db(name, quantity, description, type_id) VALUES('{name}',"
                                 f"'{quantity}','{description}',(SELECT id FROM types WHERE type = '{type}'))")
                self.references.commit()
                self.deleteLater()
                self.parent.update_results()
            else:
                self.description_label.setText('Введите формулу в корректном формате.')
                self.description_label.setAutoFillBackground(True)
                label_palette = self.description_label.palette()
                label_palette.setColor(self.description_label.backgroundRole(), Qt.red)
                self.description_label.setPalette(label_palette)
        else:
            self.description_label.setText('Введите данные.')
            self.description_label.setAutoFillBackground(True)
            label_palette = self.description_label.palette()
            label_palette.setColor(self.description_label.backgroundRole(), Qt.red)
            self.description_label.setPalette(label_palette)
