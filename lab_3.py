import numpy as np
import concurrent.futures
import multiprocessing

def gauss_forward(matrix, b, n, k):
    """
    Выполняет одну итерацию прямого хода метода Гаусса для строки k.
    """
    for i in range(k + 1, n):
        factor = matrix[i, k] / matrix[k, k]
        matrix[i, k:] -= factor * matrix[k, k:]
        b[i] -= factor * b[k]

def gauss_backward(matrix, b, x, n, k):
    """
    Выполняет одну итерацию обратного хода метода Гаусса для строки k.
    """
    x[k] = (b[k] - np.dot(matrix[k, k + 1:], x[k + 1:])) / matrix[k, k]

def parallel_gauss(A, b):
    """
    Решает систему линейных уравнений Ax = b методом Гаусса с распараллеливанием.
    """
    n = A.shape[0]
    matrix = A.copy()
    rhs = b.copy()
    
    # Прямой ход
    for k in range(n):
        with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = []
            for i in range(k + 1, n):
                futures.append(executor.submit(gauss_forward, matrix, rhs, n, k))
            concurrent.futures.wait(futures)
    
    # Обратный ход
    x = np.zeros(n)
    for k in range(n - 1, -1, -1):
        with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            executor.submit(gauss_backward, matrix, rhs, x, n, k)
    
    return x

# Пример использования
if __name__ == "__main__":
    n = 5  # Размер системы
    np.random.seed(42)
    A = np.random.rand(n, n) * 10  # Случайная матрица A
    b = np.random.rand(n) * 10     # Случайный вектор b

    print("Матрица A:")
    print(A)
    print("\nВектор b:")
    print(b)

    solution = parallel_gauss(A, b)
    print("\nРешение x:")
    print(solution)

    residual = np.dot(A, solution) - b
    print("Остаток:", residual)
