import numpy as np
import concurrent.futures

def gauss_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Поиск максимального элемента в текущем столбце
        max_row = np.argmax(abs(A[i:, i])) + i
        A[[i, max_row]] = A[[max_row, i]]
        b[[i, max_row]] = b[[max_row, i]]

        # Параллельное выполнение прямого хода
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for j in range(i + 1, n):
                futures.append(executor.submit(eliminate_row, A, b, i, j))
            concurrent.futures.wait(futures)

    return A, b

def eliminate_row(A, b, i, j):
    factor = A[j, i] / A[i, i]
    A[j, i:] -= factor * A[i, i:]
    b[j] -= factor * b[i]
# ----
def back_substitution(A, b):
    n = len(b)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]
    return x

def solve_linear_system(A, b):
    A, b = gauss_elimination(A, b)
    x = back_substitution(A, b)
    return x
# ----
if __name__ == "__main__":
    # Пример случайной СЛАУ
    n = 4
    A = np.random.rand(n, n)
    b = np.random.rand(n)

    print("Матрица A:")
    print(A)
    print("Вектор b:")
    print(b)

    x = solve_linear_system(A, b)

    print("Решение x:")
    print(x)
# ----
import matplotlib.pyplot as plt
import time

def measure_performance(A, b, num_threads):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(solve_linear_system, A, b) for _ in range(num_threads)]
        concurrent.futures.wait(futures)
    end_time = time.time()
    return end_time - start_time

def plot_performance(A, b):
    num_threads_list = list(range(1, 11))
    times = []
    for num_threads in num_threads_list:
        times.append(measure_performance(A, b, num_threads))

    plt.plot(num_threads_list, times, marker='o')
    plt.xlabel('Число потоков')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Зависимость времени выполнения от числа потоков')
    plt.show()

if __name__ == "__main__":
    n = 4
    A = np.random.rand(n, n)
    b = np.random.rand(n)

    plot_performance(A, b)
