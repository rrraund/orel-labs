import numpy as np
import matplotlib.pyplot as plt

matrix = np.array([[0.3, 0.4, 0, 0, 0.3, 0, 0, 0,],
        [0.3, 0.5, 0.2, 0, 0, 0, 0, 0,],
        [0, 0, 0.3, 0.7, 0, 0, 0, 0,],
        [0, 0, 0, 0.5, 0.5, 0, 0, 0,],
        [0, 0, 0, 0, 0.1, 0.3, 0.15, 0.45,],
        [0.6, 0, 0, 0, 0, 0.1, 0, 0.3,],
        [0, 0.25, 0, 0, 0, 0, 0.75, 0,],
        [0, 0.35, 0, 0, 0, 0, 0.3, 0.35,]])
vector1 = np.array([0, 0, 0, 1, 0, 0, 0, 0])
vector2 = np.array([1, 0, 0, 0, 0, 0, 0, 0])
epsilon = 0.0001
step = 1
mse = 1


def solve(vector, matrix, step, mse, epsilon):
    print('Solution for state vector', vector)
    mse_values = []
    x_values = []
    while mse > epsilon:
        powered_matrix = np.linalg.matrix_power(matrix, step)  # возведение матрицы в степень
        new_vector = vector.dot(powered_matrix)  # скалярное произведенеие
        mse = np.linalg.norm(vector - new_vector)

        mse_values.append(mse)
        x_values.append(step)

        vector = new_vector
        step += 1

    plt.title("Среднеквадратическое отклонение")
    plt.xlabel("Иттерация")
    plt.ylabel("Отклонение между $\pi$^(n-1) и $\pi$^n")
    plt.plot(x_values, mse_values, 'r')
    plt.show()

    print(vector, '\n')
    return vector


def analytics(matrix, n):
    matrix_this = matrix.T
    matrix_this -= np.eye(n)
    matrix_this[0] = np.ones(n)
    vector_analytics = np.zeros((n,))
    vector_analytics[0] = 1
    result = np.linalg.solve(matrix_this, vector_analytics)  # решение системы

    #Нормировка
    #normal = (result.dot(result))**(0.5)
    #if (np.sum(result) > 1):
       # result = [i/normal for i in result]
    #print(normal)

    print('Analytics solution for state vector', vector_analytics)
    print(result)


vector1_new = solve(vector1, matrix, step, mse, epsilon)
vector2_new = solve(vector2, matrix, step, mse, epsilon)
analytics(matrix, 8)

print('Среднеквадратическое отклонение для разных первоначальных условий:', np.linalg.norm(vector1_new - vector2_new))