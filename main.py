from design.interface2 import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from dihotomy import DihotomyDecision
import pyqtgraph as pg


class DihotomyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DihotomyApp, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Найти экстремум функции')

        self.graphic.setBackground('white')
        self.do_button.clicked.connect(self.do_button_clicked)
        self.shab1button.clicked.connect(self.shab1button_clicked)
        self.shab2button.clicked.connect(self.shab2button_clicked)
        self.drop_all_button.clicked.connect(self.drop_all_clicked)

        self.func_finder = None
        self.step_counter = 0

        self.graphic_label.setText('Метод дихотомии')
        self.statusbar.setFont(QtGui.QFont('Times', 15))

        self.begin_borders = None
        self.begin_sizes = None

        self.eps_spinBox.textChanged.connect(self.setEPStext)

    def do_button_clicked(self):
        function = self.func_line.text()  # get func text
        if not function:  # no func exists
            self.statusbar.show()
            self.statusBar().setStyleSheet("background-color : red;")
            self.statusbar.showMessage('Не заполнена функция!')
            return
        eps = 0.1 ** self.eps_spinBox.value()
        border = [self.left_border_SpinBox.value(), self.right_border_SpinBox.value()]
        if border[0] == border[1]:  # no borders
            self.statusbar.show()
            self.statusBar().setStyleSheet("background-color : red")
            self.statusbar.showMessage('Заданы неверные границы определения!')
            return
        self.statusbar.hide()

        to_max = self.max_radioButton.isChecked()

        if ((self.func_finder is None or self.func_finder.function != function.replace(':', '/').replace('^', '**')) or
                (not (self.func_finder is None) and
                 self.func_finder.function != function.replace(':', '/').replace('^', '**'))):
            self.graphic_label.setText('Метод дихотомии')

            self.graphic.clear()
            self.step_counter = 0
            self.func_finder = DihotomyDecision(function, border, eps)
            total_graphic_points = self.func_finder.get_points()
            self.graphic.plot([x[0] for x in total_graphic_points], [y[1] for y in total_graphic_points],
                              pen=pg.mkPen(color=(255, 0, 0), width=3))

            func_resY = [sorted((-self.func_finder.get_func_res(self.func_finder.border[i])[1],
                                 self.func_finder.get_func_res(self.func_finder.border[i])[1]))
                         for i in range(2)]
            for i, yy in enumerate(func_resY):
                yys = [y for y in range(int(yy[0] - 1000), int(yy[1] + 1000), 5)]
                self.graphic.plot([self.func_finder.border[i] for _ in range(len(yys))], yys,
                                  pen=pg.mkPen(color=(255, 255, 0), width=2, style=QtCore.Qt.DashLine))

            self.begin_borders = self.func_finder.border
        if self.full_decision_radio.isChecked():
            self.draw_fully(to_max)
        elif self.step_decision_radio.isChecked():
            self.draw_by_step(to_max)

    def draw_fully(self, to_max):
        new_graphic_borders = self.func_finder.find_extremum(to_max)[0]
        func_resY = [sorted((-self.func_finder.get_func_res(new_graphic_borders[i])[1],
                             self.func_finder.get_func_res(new_graphic_borders[i])[1]))
                     for i in range(2)]
        for i, yy in enumerate(func_resY):
            yys = [y for y in range(int(yy[0] - 1000), int(yy[1] + 1000))]
            self.graphic.plot([new_graphic_borders[i] for _ in range(len(yys))], yys,
                              pen=pg.mkPen(color=(0, 0, 255), width=2, style=QtCore.Qt.DashLine))
        self.statusBar().setStyleSheet("background-color : green")
        self.statusbar.show()
        self.statusbar.showMessage(
            f'Найден экстремум: в пределах от {min(self.func_finder.border)} до {max(self.func_finder.border)}. '
            f'Итерации: {self.func_finder.counter}.')
        print(self.func_finder.rounder)
        self.graphic_label.setText(f'y = {self.func_finder.function}, '
                                   f'{"минимум" if self.min_radioButton.isChecked() else "максимум"}\n'
                                   f'Х1 = {self.func_finder.border[0]}; '
                                   f'У1 = {round(self.func_finder.get_func_res(self.func_finder.border[0])[1], self.func_finder.rounder)}\n'
                                   f'Х2 = {self.func_finder.border[1]}; '
                                   f'У2 = {round(self.func_finder.get_func_res(self.func_finder.border[1])[1], self.func_finder.rounder)}')

    def draw_by_step(self, to_max):
        is_answer = self.func_finder.find_by_step(to_max)
        func_resY = [sorted((-self.func_finder.get_func_res(self.func_finder.border[i])[1],
                             self.func_finder.get_func_res(self.func_finder.border[i])[1]))
                     for i in range(2)]
        for i, yy in enumerate(func_resY):
            yys = [y for y in range(int(yy[0] - 1000), int(yy[1] + 1000), 5)]
            print(self.begin_borders, func_resY)
            if not is_answer:
                if self.func_finder.border[i] == self.begin_borders[i]:
                    continue
                self.graphic.plot([self.func_finder.border[i] for _ in range(len(yys))], yys,
                                  pen=pg.mkPen(color=(0, 0, 255), width=2, style=QtCore.Qt.DashLine))
            else:
                self.graphic.plot([self.func_finder.border[i] for _ in range(len(yys))], yys,
                                  pen=pg.mkPen(color=(0, 255, 0), width=2, style=QtCore.Qt.DashLine))
        if is_answer:
            self.statusBar().setStyleSheet("background-color : green")
            self.statusbar.show()
            self.statusbar.showMessage(
                f'Найден экстремум: в пределах от {min(self.func_finder.border)} до {max(self.func_finder.border)}. '
                f'Итерации: {self.func_finder.counter}.')
        else:
            self.statusBar().setStyleSheet("background-color : green")
            self.statusbar.show()
            self.statusbar.showMessage(
                f'Итерация: {self.func_finder.counter}')

    def shab1button_clicked(self):
        self.func_line.setText(self.shab1button.text().split(';')[0])
        self.left_border_SpinBox.setValue(float(self.shab1button.text().split(';')[1].split('[')[1]))
        self.right_border_SpinBox.setValue(float(self.shab1button.text().split(';')[2].split(']')[0]))

    def shab2button_clicked(self):
        self.func_line.setText(self.shab2button.text().split(';')[0])
        self.left_border_SpinBox.setValue(float(self.shab2button.text().split(';')[1].split('[')[1]))
        self.right_border_SpinBox.setValue(float(self.shab2button.text().split(';')[2].split(']')[0]))

    def drop_all_clicked(self):
        self.graphic_label.setText('Метод дихотомии')

        self.graphic.clear()
        self.func_finder = None
        self.step_counter = 0

        self.func_line.setText('x + 1')
        self.eps_spinBox.setValue(3)
        self.left_border_SpinBox.setValue(-100)
        self.right_border_SpinBox.setValue(100)
        self.full_decision_radio.toggle()
        self.min_radioButton.toggle()

    def setEPStext(self):
        self.eps_label.setText(f"Точность: 0.{'0' * (self.eps_spinBox.value() - 1)}1")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    form = DihotomyApp()
    form.show()
    sys.exit(app.exec_())
