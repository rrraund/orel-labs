import numpy as np
import math


class SimplexMethod:
    def __init__(self, c, A, b):
        self.table = np.c_[A, b]  # Симплекс-таблица, которую мы строим
        self.c = np.append(c, 0)
        self._find_basis()  # Определяет изначальный базис (набор переменных, которые будут выражены через ограничения)
        self._check_negative_b()
        self._update_deltas()

    def _is_basic(self, col_row):
        return sum(col_row) == 1 and len([c for c in col_row if c == 0]) == len(col_row) - 1

    def _pivot_step(self, pivot_position):  # Меняем в симплекс-таблице свободные переменные на базисные
        new_table = np.zeros(shape=self.table.shape)
        i, j = pivot_position
        pivot_value = self.table[i][j]
        new_table[i] = np.array(self.table[i]) / pivot_value  # Делим строку опроного элемента на него самого
        for eq_i, eq in enumerate(self.table):
            if eq_i != i:
                multiplier = np.array(new_table[i]) * self.table[eq_i][j] # Метод исключения Гаусса-Жордана
                new_table[eq_i] = np.array(self.table[eq_i]) - multiplier
        self.basis[i] = j
        self.table = new_table

    def _find_basis(self):  # Подготвока к дальнейшему решению
        self.basis = [-1] * (self.table.shape[0])
        for i, row in enumerate(self.table): # Индекс и значение/ строчка и значения в строчке
            column_j = next(j for j, x in enumerate(row) if x != 0 and j not in self.basis) # Еще не использовали для базиса (чтобы не делал базис одного вида)
            self._pivot_step((i, column_j))

    def _check_negative_b(self, maxiter=1000):  # Среди свободных коэфициентов не должно быть отрицательных чисел
        b = self.table[:, -1]
        it = 0
        while it < maxiter + 1:
            if all(x >= 0 for x in b):
                return
            max_b = max(b.min(), b.max(), key=abs)
            i = np.where(max_b)[0][0]
            row = self.table[i][:-1]
            if not any(x < 0 for x in row):
                raise Exception("No solution. No negative number in row.")
            max_row = max(row.min(), row.max(), key=abs)
            j = np.where(max_row)[0][0]
            self._pivot_step((i, j))
            b = self.table[:, -1]
            it += 1
        if it == maxiter:
            raise Exception("No solution. Maxiter exceeded")

    def _update_deltas(self):  # Видоизменяем дельты
        ci = np.array([self.c[i] for i in self.basis])
        deltas = []
        for j in range(self.table.shape[1]):
            d = self.table[:, j] @ ci.T - self.c[j]  # @ - перемножение матриц
            deltas += [d]
        D = np.array(deltas)
        self.D = D

    def _can_max_progress(self):
        D = self.D[:-1]
        return any(d for d in D if d < 0) # Хотя бы один элемент отрицательный в дельта

    def _get_max_position(self):  # Координаты опорного элемента (пайвота)
        D = self.D[:-1] # не берем дельту для b (значение целевой функции)
        column = np.argmin(D)
        xj = self.table[:, column]  # выделили столб
        b = self.table[:, -1]  # свободные коэффициенты
        simplex_Q = [math.inf if x <= 0 else b[i] / x for i, x in enumerate(xj)]
        # Набор отношений свободных коэффициентов к иксу / присваиваем бесконечность, для того чтобы проверить условие
        if (all([r == math.inf for r in simplex_Q])):
            raise Exception("Linear program is unbounded.")
        row = simplex_Q.index(min(simplex_Q))
        return row, column

    def maximize(self):  # Максимазация функции
        while self._can_max_progress():  # Ищем до тех пор пока есть решение
            position = self._get_max_position()
            self._pivot_step(position)
            self._update_deltas()
        return self._get_solution()

    def minimize(self):
        self.c *= -1
        solution = self.maximize()
        self.c *= -1
        return solution

    def _get_solution(self):
        solution = np.zeros(shape=self.c.shape)
        for i in self.basis:
            one_index = np.where(self.table[:, i] == 1)[0][0] #
            solution[i] = self.table[:, -1][one_index]
        return solution

    def function_value(self, X):
        return self.c @ X.T



def parse_file(path):
    file = open(path, "r")
    data = file.readlines()
    с = data[-1].replace('\n', '').split(' ')
    с = [float(x) for x in с]
    A = []
    b = []
    for i in range(len(data) - 1):
        A.append(data[i].replace('\n', '').split(' '))
        b.append(A[i][-2:])
        b[i][1] = float(b[i][1])
        b[i] = A[i][:len(A[i]) - 2]
        A[i] = [float(x) for x in A[i]]
    return np.asarray(A), b, с


def main():
    #4
    c = np.array([-1, -1, -1, 1, -1])  # Коэффиценты функции
    A = np.array([[1, 1, 2, 0, 0],
                  [0, -2, -2, 1, -1],
                  [1, -1, 6, 1, 1]])  # Ограничения
    b = np.array([4, -6, 12])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.minimize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))



def main2():
    c = np.array([80, 156, 84, 169, 0])  # Коэффиценты функции
    A = np.array([[1, 1, 1, 1, 1],
                  [10, 13, 0, 0, 0],
                  [0, 0, 12, 13, 0]])  # Ограничения
    b = np.array([24, 230, 68])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.minimize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))



def main2_():
    c = np.array([1, 1, 0, 0])  # Коэффиценты функции
    A = np.array([[0, 50, 1, 0],
                  [100, 0, 0, 1]])  # Ограничения
    b = np.array([1, 1])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.minimize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))


def main3():
    c = np.array([12, 8, 0, 0, 0, 0])  # Коэффициенты функции
    A = np.array([[1, 1, -1, 0, 0, 0],
                  [2, 1, 0, -1, 0, 0],
                  [5, 4, 0, 0, -1, 0],
                  [4, 1, 0, 0, 0, -1]] )  # Ограничения
    b = np.array([60, 80, 40, 100])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.minimize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))


def main4():
    c = np.array([1, 1, 1, 0, 0])  # Коэффиценты функции
    A = np.array([[8, 4, 6, -1, 0],
                  [4, 8, 5, 0, -1]] )  # Ограничения
    b = np.array([1, 1])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.minimize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))


def main5():
    c = np.array([1, 1, 1, 1, 0, 0, 0, 0])  # Коэффиценты функции
    A = np.array([[90, 76.5, 91.5, 91.5, 1, 0, 0, 0],
                  [103.5, 90, 91.5, 103.5, 0, 1, 0, 0],
                  [88.5, 88.5, 90, 103.5, 0, 0, 1, 0],
                  [88.5, 76.5, 76.5, 90, 0, 0, 0, 1]] )  # Ограничения
    b = np.array([1, 1, 1, 1])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.maximize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))

def main6():
    c = np.array([1, 1, 1, 1, 0, 0, 0, 0])  # Коэффиценты функции
    A = np.array([[60, 46.5, 61.5, 61.5, 1, 0, 0, 0],
                  [73.5, 60, 61.5, 73.5, 0, 1, 0, 0],
                  [58.5, 58.5, 60, 73.5, 0, 0, 1, 0],
                  [58.5, 46.5, 46.5, 60, 0, 0, 0, 1]] )  # Ограничения
    b = np.array([1, 1, 1, 1])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.maximize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))

def main7():
    c = np.array([1, 1, 0, 0, 0])  # Коэффиценты функции
    A = np.array([[3, 5, 1, 0, 0],
                  [4, -3, 0, 1, 0],
                  [1, -3, 0, 0, -1]])  # Ограничения
    b = np.array([30, 12, 6])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.maximize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))

def main8():
    c = np.array([1, 1, 0, 0])  # Коэффиценты функции
    A = np.array([[-100, 50, -1, 0],
                  [100, -100, 0, -1]])  # Ограничения
    b = np.array([1, 1])  # Свободные коэффициенты

    simplex = SimplexMethod(c, A, b)

    min_x = simplex.maximize()
    print(f'min_x = {min_x}')
    print('f(min_x) = {:.2f}'.format(simplex.function_value(min_x)))


main()
#main2()
#main3()
#main4()
#main5()
#main6()
#main8()
#main2_()
