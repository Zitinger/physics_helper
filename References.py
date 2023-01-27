import sqlite3
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QStatusBar, QTableWidgetItem, QMessageBox
from AddNewReference import AddNewReference
from OpenReference import OpenReference


class References(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis/references.ui', self)
        self.type = '"формула"'
        self.find_by = 'name'
        self.result_bar = QStatusBar(self)
        self.references = sqlite3.connect("references.sqlite")
        self.cur = self.references.cursor()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Справочный материал')

        self.result_bar.setAutoFillBackground(True)
        self.result_bar.resize(880, 4)
        self.result_bar.move(10, 840)

        self.openBtn.clicked.connect(self.open_reference)
        self.addBtn.clicked.connect(self.add_reference)
        self.removeBtn.clicked.connect(self.remove_reference)
        self.formula_radioBtn.clicked.connect(self.radio_btn_changed)
        self.laws_radioBtn.clicked.connect(self.radio_btn_changed)
        self.definition_radioBtn.clicked.connect(self.radio_btn_changed)
        self.name_radioBtn.clicked.connect(self.radio_btn_changed)
        self.description_radioBtn.clicked.connect(self.radio_btn_changed)
        self.quantity_radioBtn.clicked.connect(self.radio_btn_changed)
        self.lineEdit.textChanged.connect(self.update_results)

        self.update_results()

    def open_reference(self):
        try:
            row = self.tableWidget.currentRow()
            r_name = self.tableWidget.item(row, 1).text()
            r_description = self.tableWidget.item(row, 2).text()
            r_type = self.type[1:-1].capitalize()
            self.reference = OpenReference(r_name, r_description, r_type)
            self.reference.show()
        except AttributeError:
            print('Выберите запись, которую хотите открыть')

    def add_reference(self):
        self.add_new_reference = AddNewReference(self)
        self.add_new_reference.show()

    def remove_reference(self):
        try:
            row = self.tableWidget.currentRow()
            id = self.tableWidget.item(row, 0).text()

            s = self.type[1:-1]
            if self.type == '"формула"':
                s = self.type[1:7] + 'у'

            valid = QMessageBox.question(self, 'Подтвердите операцию', f"Действительно удалить {s}?",
                                         QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.cur.execute(f'DELETE FROM references_db WHERE id = {id}')
                self.references.commit()
                self.update_results()
        except AttributeError:
            print('Выберите запись, которую хотите удалить')

    def radio_btn_changed(self):
        if self.sender() == self.formula_radioBtn:
            self.type = '"формула"'
            self.quantity_radioBtn.setHidden(False)
        elif self.sender() == self.laws_radioBtn:
            self.type = '"закон"'
            self.quantity_radioBtn.setHidden(True)
            self.name_radioBtn.setChecked(True)
            self.find_by = 'name'
        elif self.sender() == self.definition_radioBtn:
            self.type = '"определение"'
            self.quantity_radioBtn.setHidden(True)
            self.name_radioBtn.setChecked(True)
            self.find_by = 'name'
        elif self.sender() == self.name_radioBtn:
            self.find_by = 'name'
        elif self.sender() == self.description_radioBtn:
            self.find_by = 'description'
        elif self.sender() == self.quantity_radioBtn:
            self.find_by = 'quantity'
        self.update_results()

    def update_results(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        if self.lineEdit.text().strip() != '':
            res = self.cur.execute(f'SELECT id, name, description FROM references_db '
                                   f'WHERE type_id = (SELECT id FROM types WHERE type={self.type}) AND'
                                   f' {self.find_by} like "%{self.lineEdit.text().lower()}%"').fetchall()
        else:
            res = self.cur.execute(f'SELECT id, name, description FROM references_db ' +
                                   f'WHERE type_id = (SELECT id FROM types WHERE type={self.type})').fetchall()

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 2:
                    if not str(elem).isdigit() and str(elem)[2] != '=' and str(elem)[3] != '=':
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(str(elem).capitalize()))
                    else:
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(str(elem)))
                else:
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem).capitalize()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.remove_reference()
