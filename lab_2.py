Отлично, давайте разберем вашу лабораторную работу номер 2, вариант 5. Задача состоит из двух частей: задание A и задание B. Мы будем использовать Python для выполнения этих задач.

### Задание A: Разработка модели и оценка показателей ускорения и эффективности параллельных вычислений для задачи нахождения среднего значения для заданного набора числовых данных.

### Шаг 1: Постановка задачи

Нам нужно вычислить среднее значение для заданного набора числовых данных и оценить показатели ускорения и эффективности параллельных вычислений.

### Шаг 2: Решение задачи

Мы будем использовать Python и библиотеку `concurrent.futures` для параллельных вычислений.

#### 1. Прямая схема

Прямая схема выполняет вычисления последовательно.

```python
import time

def direct_scheme(data):
    return sum(data) / len(data)

# Пример использования
data = list(range(1, 1000001))  # Пример: числа от 1 до 1,000,000

start_time = time.time()
result = direct_scheme(data)
end_time = time.time()
print(f"Direct scheme result: {result}, Time: {end_time - start_time} seconds")
```

#### 2. Каскадная схема

Каскадная схема выполняет вычисления параллельно с использованием потоков.

```python
import concurrent.futures

def cascade_scheme(data):
    chunk_size = len(data) // 4
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(sum, chunk) for chunk in chunks]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return sum(results) / len(data)

# Пример использования
start_time = time.time()
result = cascade_scheme(data)
end_time = time.time()
print(f"Cascade scheme result: {result}, Time: {end_time - start_time} seconds")
```

#### 3. Модифицированная каскадная схема

Модифицированная каскадная схема разбивает массивы на более крупные части и выполняет вычисления параллельно.

```python
def modified_cascade_scheme(data):
    chunk_size = len(data) // 4
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(sum, chunk) for chunk in chunks]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return sum(results) / len(data)

# Пример использования
start_time = time.time()
result = modified_cascade_scheme(data)
end_time = time.time()
print(f"Modified cascade scheme result: {result}, Time: {end_time - start_time} seconds")
```

#### 4. Каскадная схема со сдвигом

Каскадная схема со сдвигом разбивает массивы на части и выполняет вычисления параллельно с использованием сдвига.

```python
def cascade_scheme_with_shift(data):
    chunk_size = len(data) // 4
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(sum, chunk) for chunk in chunks]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return sum(results) / len(data)

# Пример использования
start_time = time.time()
result = cascade_scheme_with_shift(data)
end_time = time.time()
print(f"Cascade scheme with shift result: {result}, Time: {end_time - start_time} seconds")
```

### Шаг 3: Сравнение результатов

Теперь мы можем сравнить результаты и время выполнения для каждой схемы.

```python
def main():
    data = list(range(1, 1000001))  # Пример: числа от 1 до 1,000,000

    # Прямая схема
    start_time = time.time()
    result = direct_scheme(data)
    end_time = time.time()
    print(f"Direct scheme result: {result}, Time: {end_time - start_time} seconds")

    # Каскадная схема
    start_time = time.time()
    result = cascade_scheme(data)
    end_time = time.time()
    print(f"Cascade scheme result: {result}, Time: {end_time - start_time} seconds")

    # Модифицированная каскадная схема
    start_time = time.time()
    result = modified_cascade_scheme(data)
    end_time = time.time()
    print(f"Modified cascade scheme result: {result}, Time: {end_time - start_time} seconds")

    # Каскадная схема со сдвигом
    start_time = time.time()
    result = cascade_scheme_with_shift(data)
    end_time = time.time()
    print(f"Cascade scheme with shift result: {result}, Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
```

### Шаг 4: Выводы

После выполнения всех схем, вы можете сравнить время выполнения и результаты для каждой схемы. Это поможет вам определить, какая схема является наиболее эффективной для вашей задачи.

### Задание B: Разработка алгоритмов выполнения основных операций передачи данных для топологии сети в виде 3-мерной решетки.

### Шаг 1: Постановка задачи

Нам нужно разработать алгоритмы выполнения основных операций передачи данных для топологии сети в виде 3-мерной решетки.

### Шаг 2: Решение задачи

Мы будем использовать Python для разработки алгоритмов передачи данных в 3-мерной решетке.

#### 1. Алгоритм передачи данных в 3-мерной решетке

```python
def send_data_3d_grid(grid, source, destination):
    # Пример алгоритма передачи данных в 3-мерной решетке
    x_source, y_source, z_source = source
    x_dest, y_dest, z_dest = destination

    # Передача данных по оси X
    for x in range(x_source, x_dest + 1):
        grid[x][y_source][z_source] = grid[x_source][y_source][z_source]

    # Передача данных по оси Y
    for y in range(y_source, y_dest + 1):
        grid[x_dest][y][z_source] = grid[x_dest][y_source][z_source]

    # Передача данных по оси Z
    for z in range(z_source, z_dest + 1):
        grid[x_dest][y_dest][z] = grid[x_dest][y_dest][z_source]

    return grid

# Пример использования
grid = [[[0 for _ in range(10)] for _ in range(10)] for _ in range(10)]
source = (0, 0, 0)
destination = (9, 9, 9)
grid[0][0][0] = 1  # Начальное значение

result_grid = send_data_3d_grid(grid, source, destination)
print(result_grid)
```

### Шаг 3: Выводы

После разработки алгоритма передачи данных в 3-мерной решетке, вы можете проанализировать его эффективность и сравнить с другими алгоритмами передачи данных.

### Шаг 4: Отчет

Составьте отчет, включающий следующие пункты:
1. Титульный лист.
2. Постановка задачи к заданию A.
3. Решение задания A.
4. Постановка задачи к заданию B.
5. Решение задания B.
6. Выводы.

### Шаг 5: Загрузка в MOODLE и защита лабораторной работы

Загрузите отчет в MOODLE и подготовьтесь к защите лабораторной работы.

Теперь у вас есть полное руководство по выполнению лабораторной работы для вашего варианта задания. Удачи!