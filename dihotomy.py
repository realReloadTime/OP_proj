from time import sleep
from math import sin, cos, tan
import numpy as np


class DihotomyDecision:
    def __init__(self, function: str, border: list, eps: float):
        self.function = function
        self.border = [min(border), max(border)]
        self.eps = eps
        self.rounder = 3

        self.function = self.function.replace(':', '/').replace('^', '**')
        self.counter = 0

    def get_func_res(self, x):
        try:
            return x, eval(self.function.replace('x', f'({x})'))
        except ZeroDivisionError:
            return x, 0

    def move_border(self, to_max=False):
        self.border = [min(self.border), max(self.border)]
        to_max = 1 if not to_max else -1

        c = round((self.border[0] + self.border[1]) / 2, self.rounder)
        x1 = c - self.eps
        x2 = c + self.eps

        f1 = round(self.get_func_res(x1)[1], self.rounder)
        f2 = round(self.get_func_res(x2)[1], self.rounder)

        if to_max * f1 < to_max * f2:
            self.border[1] = c
        else:
            self.border[0] = c

        return c, x1, x2, f1, f2, self.rounder, self.border

    def find_extremum(self, to_max=False):
        self.set_rounder()
        while abs(self.border[1] - self.border[0]) >= self.eps:
            self.move_border(to_max)
            self.counter += 1
        return self.border, self.eps

    def find_by_step(self, to_max=False):
        self.set_rounder()
        if abs(self.border[1] - self.border[0]) >= self.eps:
            self.move_border(to_max)
            self.counter += 1
            return False
        else:
            return True

    def set_rounder(self, count=0):
        if count != 0:
            self.rounder = count
            return
        temp_eps = self.eps
        if self.rounder > 3:
            return
        while temp_eps < 1:
            temp_eps *= 10
            self.rounder += 1

    def get_points(self):
        if self.rounder == 1:
            self.set_rounder()
        points = np.array(list(map(lambda x: self.get_func_res(x / 10 ** self.rounder),
                                   range(int(min(self.border) * 10 ** self.rounder),
                                         int(max(self.border) * 10 ** self.rounder) + 1, 10 ** abs(self.rounder - 2)))))
        return points


if __name__ == '__main__':
    print("Введите функцию: ", end='')
    test = DihotomyDecision(input(), [-3, -1], 0.001)
    print(test.get_points())
    print(test.find_extremum(True))
