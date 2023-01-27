from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QStatusBar
from PyQt5.QtWidgets import QColorDialog
import pyqtgraph as pg


class Graph(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis/graph.ui', self)
        self.result_bar = QStatusBar(self)
        self.pen = pg.mkPen(color=(255, 255, 255))
        self.initUI()

    def initUI(self):
        self.setWindowTitle('График')

        self.square_txt.setHidden(True)

        self.result_bar.setAutoFillBackground(True)
        self.result_bar.resize(826, 8)
        self.result_bar.move(10, 814)

        self.radioButton_s.toggled.connect(self.radio_button_changed)

        self.v0_spinBox.valueChanged.connect(self.spinBox_changed)
        self.a_spinBox.valueChanged.connect(self.spinBox_changed)

        self.colorBtn.clicked.connect(self.change_pen_color)
        self.buildBtn.clicked.connect(self.build)

    def change_pen_color(self):
        color = QColorDialog.getColor()
        self.pen = pg.mkPen(color=color.name())
        if self.finally_formula_txt.text() != 'Введите данные':
            self.build()

    def build(self):
        bar_palette = self.result_bar.palette()
        self.graph_widget.clear()
        s = self.finally_formula_txt.text()[7:]
        if s != ' данные':
            s = s.replace('t', ' * t').replace('t2', 't ** 2')
            self.graph_widget.plot([i for i in range(30)], [eval(s.replace('t', str(i))) for i in range(30)],
                                   pen=self.pen)
            bar_palette.setColor(self.result_bar.backgroundRole(), Qt.darkGreen)
        else:
            bar_palette.setColor(self.result_bar.backgroundRole(), Qt.red)
        self.result_bar.setPalette(bar_palette)

    def radio_button_changed(self):
        if self.sender().isChecked():
            self.square_txt.setHidden(False)
            self.zero_txt.move(410, 154)
            self.v0_spinBox.setValue(0)
            self.a_spinBox.setValue(0)
            self.basic_formula_txt.setText('s(t) = v t + 0.5at ')
        else:
            self.square_txt.setHidden(True)
            self.zero_txt.move(433, 154)
            self.v0_spinBox.setValue(0)
            self.a_spinBox.setValue(0)
            self.basic_formula_txt.setText('v(t) = v  + at')
        self.graph_widget.clear()

    def spinBox_changed(self):
        a = self.a_spinBox.value()
        v0 = self.v0_spinBox.value()
        if v0 % 1 == 0:
            v0 = int(v0)
        if a % 1 == 0:
            a = int(a)

        if self.radioButton_v.isChecked():
            if a < 0 and v0 != 0:
                self.finally_formula_txt.setText(f'v(t) = {v0} - {abs(a)}t')
            elif a > 0 and v0 != 0:
                self.finally_formula_txt.setText(f'v(t) = {v0} + {a}t')
            elif a == 0 and v0 != 0:
                self.finally_formula_txt.setText(f'v(t) = {v0}')
            elif a != 0 and v0 == 0:
                self.finally_formula_txt.setText(f'v(t) = {a}t')
            elif a == 0 and v0 == 0:
                self.finally_formula_txt.setText('Введите данные')
        else:
            a = a * 0.5
            if a % 1 == 0:
                a = int(a)

            if a < 0 and v0 != 0:
                self.finally_formula_txt.setText(f's(t) = {v0}t - {abs(a)}t2')
            elif a > 0 and v0 != 0:
                self.finally_formula_txt.setText(f's(t) = {v0}t + {a}t2')
            elif a == 0 and v0 != 0:
                self.finally_formula_txt.setText(f's(t) = {v0}t')
            elif a != 0 and v0 == 0:
                self.finally_formula_txt.setText(f's(t) = {a}t2')
            elif a == 0 and v0 == 0:
                self.finally_formula_txt.setText('Введите данные')

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_B, Qt.Key_Return]:
            self.build()
