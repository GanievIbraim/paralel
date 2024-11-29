import numpy as np
import concurrent.futures
import time
import os

def winograd_multiply(A, B):
    m, n = A.shape
    n, p = B.shape
    C = np.zeros((m, p))

    # Разделение матрицы A на столбцы
    def process_column(j):
        for i in range(m):
            row_sum = 0
            col_sum = 0
            for k in range(n // 2):
                row_sum += (A[i, 2 * k] + B[2 * k + 1, j]) * (A[i, 2 * k + 1] + B[2 * k, j])
                col_sum += A[i, 2 * k] * A[i, 2 * k + 1] + B[2 * k, j] * B[2 * k + 1, j]
            C[i, j] = row_sum - col_sum

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_column, j) for j in range(p)]
        concurrent.futures.wait(futures)

    return C

def main():
    # Ввод размеров матриц
    m = int(input("Введите количество строк матрицы A: "))
    n = int(input("Введите количество столбцов матрицы A: "))
    p = int(input("Введите количество столбцов матрицы B: "))

    # Проверка корректности данных
    if n != m:
        print("Количество столбцов матрицы A должно быть равно количеству строк матрицы B.")
        return

    # Генерация случайных матриц
    A = np.random.randint(0, 10, size=(m, n))
    B = np.random.randint(0, 10, size=(n, p))

    print("Матрица A:")
    print(A)
    print("Матрица B:")
    print(B)

    # Умножение матриц с использованием алгоритма Винограда
    start_time = time.time()
    C = winograd_multiply(A, B)
    end_time = time.time()

    print("Результат умножения матриц:")
    print(C)
    print(f"Время выполнения: {end_time - start_time} секунд")

if __name__ == "__main__":
    main()
