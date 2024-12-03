import numpy as np
from multiprocessing import Pool
import time

# Функция для вычисления частичных сумм
def partial_mean(data_chunk):
    partial_sum = sum(data_chunk)
    count = len(data_chunk)
    return partial_sum, count

# Параллельное вычисление среднего значения
def parallel_mean(data, num_processes):
    chunk_size = len(data) // num_processes
    chunks = [data[i * chunk_size: (i + 1) * chunk_size] for i in range(num_processes)]
    if len(data) % num_processes != 0:  # Добавляем оставшиеся данные в последний процесс
        chunks[-1].extend(data[num_processes * chunk_size:])
    
    with Pool(processes=num_processes) as pool:
        results = pool.map(partial_mean, chunks)
    
    total_sum = sum([res[0] for res in results])
    total_count = sum([res[1] for res in results])
    return total_sum / total_count

# Оценка ускорения и эффективности
def evaluate_performance(data, num_processes):
    # Последовательное выполнение
    start_seq = time.time()
    mean_seq = sum(data) / len(data)
    time_seq = time.time() - start_seq
    
    # Параллельное выполнение
    start_par = time.time()
    mean_par = parallel_mean(data, num_processes)
    time_par = time.time() - start_par

    # Проверка корректности
    assert abs(mean_seq - mean_par) < 1e-6, "Результаты последовательного и параллельного выполнения не совпадают!"

    # Расчёт ускорения и эффективности
    speedup = time_seq / time_par
    efficiency = speedup / num_processes

    return mean_par, time_seq, time_par, speedup, efficiency

# Пример использования
if __name__ == "__main__":
    N = 10**6  # Количество данных
    data = np.random.rand(N) * 100  # Генерация данных
    
    num_processes = 4
    mean, time_seq, time_par, speedup, efficiency = evaluate_performance(data, num_processes)
    
    print(f"Среднее значение: {mean}")
    print(f"Время последовательного выполнения: {time_seq:.4f} сек")
    print(f"Время параллельного выполнения: {time_par:.4f} сек")
    print(f"Ускорение: {speedup:.2f}")
    print(f"Эффективность: {efficiency:.2f}")
