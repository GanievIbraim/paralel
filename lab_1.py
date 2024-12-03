import time
from multiprocessing import Pool, cpu_count

# Функция для вычисления частичной суммы
def partial_sum(args):
    a, b, start, end = args
    return sum(a[i] * b[i] for i in range(start, end))

# Прямая схема (последовательная)
def sequential_sum_of_products(a, b):
    return sum(x * y for x, y in zip(a, b))

# Каскадная схема
def parallel_sum_of_products(a, b, num_processes):
    chunk_size = len(a) // num_processes
    ranges = [(a, b, i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    ranges[-1] = (a, b, ranges[-1][2], len(a))  # Коррекция последнего диапазона
    
    with Pool(processes=num_processes) as pool:
        partial_results = pool.map(partial_sum, ranges)
    
    return sum(partial_results)

# Модифицированная каскадная схема
def modified_cascade_sum(a, b, num_processes):
    chunk_size = len(a) // num_processes
    ranges = [(a, b, i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    ranges[-1] = (a, b, ranges[-1][2], len(a))  # Корректируем последний диапазон
    
    with Pool(processes=num_processes) as pool:
        partial_results = pool.map(partial_sum, ranges)
    
    # Объединяем частичные суммы
    while len(partial_results) > 1:
        new_results = []
        for i in range(0, len(partial_results) - 1, 2):
            new_results.append(partial_results[i] + partial_results[i + 1])
        if len(partial_results) % 2 == 1:  # Если остался один элемент
            new_results.append(partial_results[-1])
        partial_results = new_results
    
    return partial_results[0]


# Каскадная схема со сдвигом
def shifted_cascade_sum(a, b, num_processes):
    chunk_size = len(a) // num_processes
    ranges = [(a, b, i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    ranges[-1] = (a, b, ranges[-1][2], len(a))  # Корректируем последний диапазон
    
    with Pool(processes=num_processes) as pool:
        partial_results = pool.map(partial_sum, ranges)
    
    return sum(partial_results)


# Измерение производительности
def measure_performance(a, b, method, num_processes=1):
    start = time.time()
    result = method(a, b, num_processes) if num_processes > 1 else method(a, b)
    end = time.time()
    return result, end - start

if __name__ == "__main__":
    n = 10**6  # Количество элементов
    a = list(range(1, n + 1))
    b = list(range(1, n + 1))
    num_processes = cpu_count()

    print("Прямая схема:")
    seq_result, seq_time = measure_performance(a, b, sequential_sum_of_products)
    print(f"Результат: {seq_result}, Время: {seq_time:.4f} сек")

    print("\nКаскадная схема:")
    par_result, par_time = measure_performance(a, b, parallel_sum_of_products, num_processes)
    print(f"Результат: {par_result}, Время: {par_time:.4f} сек")

    print("\nМодифицированная каскадная схема:")
    mod_result, mod_time = measure_performance(a, b, modified_cascade_sum, num_processes)
    print(f"Результат: {mod_result}, Время: {mod_time:.4f} сек")

    print("\nКаскадная схема со сдвигом:")
    shift_result, shift_time = measure_performance(a, b, shifted_cascade_sum, num_processes)
    print(f"Результат: {shift_result}, Время: {shift_time:.4f} сек")
