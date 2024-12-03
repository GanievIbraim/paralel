import numpy as np
from multiprocessing import Pool
import matplotlib.pyplot as plt
import time

# Функция для прямого хода
def forward_elimination(args):
    matrix, vector, k = args
    n = len(matrix)
    for i in range(k + 1, n):
        if matrix[k, k] == 0:
            continue
        factor = matrix[i, k] / matrix[k, k]
        matrix[i, k:] -= factor * matrix[k, k:]
        vector[i] -= factor * vector[k]
    return matrix, vector

# Функция для обратного хода
def back_substitution(matrix, vector):
    n = len(matrix)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (vector[i] - np.dot(matrix[i, i + 1:], x[i + 1:])) / matrix[i, i]
    return x

# Параллельный метод Гаусса
def parallel_gauss(matrix, vector, num_processes):
    n = len(matrix)
    for k in range(n - 1):
        with Pool(processes=num_processes) as pool:
            chunks = [(matrix, vector, k) for _ in range(num_processes)]
            results = pool.map(forward_elimination, chunks)
        
        matrix, vector = results[0]  # Обновляем только один раз, так как данные идентичны

    x = back_substitution(matrix, vector)
    return x

# Оценка производительности
def evaluate_gauss(n, num_processes):
    A = np.random.rand(n, n) * 100  # Генерация случайной матрицы
    b = np.random.rand(n) * 100     # Генерация случайного вектора

    # Последовательное выполнение
    start_seq = time.time()
    x_seq = np.linalg.solve(A, b)
    time_seq = time.time() - start_seq

    # Параллельное выполнение
    start_par = time.time()
    x_par = parallel_gauss(np.copy(A), np.copy(b), num_processes)
    time_par = time.time() - start_par

    # Проверка корректности
    assert np.allclose(x_seq, x_par, atol=1e-6), "Результаты не совпадают!"

    # Ускорение и эффективность
    speedup = time_seq / time_par
    efficiency = speedup / num_processes

    return time_seq, time_par, speedup, efficiency

# Построение графиков
def plot_results(n):
    num_threads = range(1, 9)
    times_seq = []
    times_par = []
    speedups = []
    efficiencies = []

    for num_processes in num_threads:
        time_seq, time_par, speedup, efficiency = evaluate_gauss(n, num_processes)
        times_seq.append(time_seq)
        times_par.append(time_par)
        speedups.append(speedup)
        efficiencies.append(efficiency)

    # Графики
    plt.figure(figsize=(12, 6))
    
    # Ускорение
    plt.subplot(1, 2, 1)
    plt.plot(num_threads, speedups, marker='o', label="Ускорение")
    plt.axhline(1, color='red', linestyle='--', label="Линейное ускорение")
    plt.title("Ускорение")
    plt.xlabel("Число потоков")
    plt.ylabel("Ускорение")
    plt.legend()

    # Эффективность
    plt.subplot(1, 2, 2)
    plt.plot(num_threads, efficiencies, marker='o', label="Эффективность")
    plt.axhline(1, color='red', linestyle='--', label="Идеальная эффективность")
    plt.title("Эффективность")
    plt.xlabel("Число потоков")
    plt.ylabel("Эффективность")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Основная программа
if __name__ == "__main__":
    n = 500  # Размерность матрицы
    print("Анализ параллельного метода Гаусса...")
    plot_results(n)
