from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QStatusBar, QLabel
import sqlite3


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis/calculator.ui', self)
        self.formulas_dic = {}
        self.list_of_given = [[self.quan1, self.spinBox1], [self.quan2, self.spinBox2], [self.quan3, self.spinBox3],
                              [self.quan4, self.spinBox4], [self.quan5, self.spinBox5], [self.quan6, self.spinBox6],
                              [self.quan7, self.spinBox7], [self.quan8, self.spinBox8], [self.quan9, self.spinBox9],
                              [self.quan10, self.spinBox10], [self.quan11, self.spinBox11],
                              [self.quan12, self.spinBox12], [self.quan13, self.spinBox13]]

        self.result_bar = QStatusBar(self)
        self.references = sqlite3.connect("references.sqlite")
        self.cur = self.references.cursor()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Калькулятор')
        self.setGeometry(700, 100, 900, 858)
        self.resize(902, 874)

        self.result_bar.setAutoFillBackground(True)
        self.result_bar.resize(880, 8)
        self.result_bar.move(10, 860)

        self.hide_all_given()

        self.refresh_formulas_dic()
        self.refresh_quantity()
        self.refresh_formula()
        self.refresh_givenQuan()

        self.solveBtn.clicked.connect(self.solve)
        self.refreshBtn.clicked.connect(self.refresh_formulas_dic)
        self.otherQuan_comboBox.currentTextChanged.connect(self.refresh_formula)
        self.otherFormula_comboBox.currentTextChanged.connect(self.refresh_givenQuan)

    def refresh_formula(self):
        self.otherFormula_comboBox.clear()
        self.otherFormula_comboBox.addItems(self.formulas_dic[self.otherQuan_comboBox.currentText()])

    def refresh_quantity(self):
        self.otherQuan_comboBox.clear()
        self.otherQuan_comboBox.addItems(self.formulas_dic.keys())

    def refresh_formulas_dic(self):
        self.formulas_dic = {}
        res = self.cur.execute('SELECT quantity, description FROM references_db WHERE type_id = (SELECT id FROM types'
                               ' WHERE type = "формула")').fetchall()
        for k in res:
            if k[0] in self.formulas_dic.keys():
                if k[1] not in self.formulas_dic[k[0]]:
                    self.formulas_dic[k[0]].append(k[1])
            else:
                self.formulas_dic[k[0]] = [k[1]]

        self.refresh_quantity()

    def refresh_givenQuan(self):
        self.hide_all_given()
        self.dict_of_quantities = {}

        s = self.otherFormula_comboBox.currentText().replace(' ', '')
        if s.count('=') != 1:
            return

        s = list(s)
        for i in range(len(s) - 1, 0, -1):
            if s[i].isalpha() and s[i - 1].isalpha():
                s[i] = '*' + s[i]
        s = ''.join(s)

        list_of_quan = self.get_list_of_quantities(s)
        for q in list_of_quan:
            self.dict_of_quantities[q] = 0

        print(self.dict_of_quantities)

        for i in range(len(list_of_quan)):
            self.list_of_given[i][0].setHidden(False)
            self.list_of_given[i][1].setHidden(False)
            self.list_of_given[i][0].setText(list_of_quan[i] + ' =')

    def get_list_of_quantities(self, s):
        n = s.index('=')
        s = s[n + 1:].replace('+', ' + ').replace('-', ' - ').replace('*', ' * ')
        s = s.replace('^', ' ^ ').replace('/', ' / ').replace('(', ' ( ').replace(')', ' ) ')
        list_of_symbols = s.split()
        for i in range(len(list_of_symbols) - 1, -1, -1):
            symb = list_of_symbols[i]
            if symb.isdigit() or symb in '()+-/*^':
                del list_of_symbols[i]
        print(list_of_symbols)
        return list(set(list_of_symbols))

    def solve(self):
        quan_dict = self.dict_of_quantities
        keys = list(quan_dict.keys())
        s = self.otherFormula_comboBox.currentText()
        for i in range(len(keys)):
            quan_dict[keys[i]] = self.list_of_given[i][1].value()
        keys.sort(reverse=True)

        a = list(s)
        for i in range(len(a) - 1, -1, -1):
            if a[i].isalpha() and a[i - 1].isalpha() and i > 1:
                a[i] = f' * {a[i]}'
        s = ''.join(a)

        n = s.index('=')
        s1 = s[:n + 1]
        s2 = s[n + 1:]
        for i in range(len(keys)):
            s2 = s2.replace(keys[i], str(quan_dict[keys[i]]))
        s = s1 + s2

        try:
            n = s.index('=')
            res = f'{s[:n + 2]}{eval(s.replace("^", "**")[n + 2:])}'
            self.result_textEdit.setPlainText(f'Дано:\n'
                                              f'{"; ".join([f"{quan} = {value}" for quan, value in quan_dict.items()])}'
                                              f'\n\nНайти:\n{self.otherQuan_comboBox.currentText()}\n\n'
                                              f'{self.otherFormula_comboBox.currentText()}\n'
                                              f'{s}\n{res}\n\nОтвет: {res}')

            bar_palette = self.result_bar.palette()
            bar_palette.setColor(self.result_bar.backgroundRole(), Qt.darkGreen)
            self.result_bar.setPalette(bar_palette)
        except ZeroDivisionError:
            self.result_textEdit.setPlainText(f'Дано:\n'
                                              f'{"; ".join([f"{quan} = {value}" for quan, value in quan_dict.items()])}'
                                              f'\n\nНайти:\n{self.otherQuan_comboBox.currentText()}\n\n'
                                              f'{self.otherFormula_comboBox.currentText()}\n'
                                              f'{s}\nДеление на ноль!!!')

            bar_palette = self.result_bar.palette()
            bar_palette.setColor(self.result_bar.backgroundRole(), Qt.darkRed)
            self.result_bar.setPalette(bar_palette)

    def hide_all_given(self):
        for pair in self.list_of_given:
            for widget in pair:
                widget.setHidden(True)

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_F]:
            self.solve()

