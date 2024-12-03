import multiprocessing as mp
import os
import time
import numpy as np
from datetime import datetime

# Функция для проверки введённых данных
def validate_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Ошибка: введите положительное целое число.")

# Функция умножения матрицы A на столбец B
def multiply_column(args):
    A, B, col_index, process_id, parent_id, delay = args  # Распаковка аргументов
    n_rows = A.shape[0]
    result = np.zeros(n_rows)

    for i in range(n_rows):
        result[i] = np.dot(A[i, :], B[:, col_index])

    # Вывод информации о процессе
    while True:
        print(
            f"Процесс {process_id} | PID: {os.getpid()} | PPID: {parent_id} | "
            f"Время: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}"
        )
        time.sleep(delay / 1000)  # Задержка в секундах

    return result


# Основная программа
def main():
    print("Программа для умножения матриц с параллелизацией по столбцам.")

    # Ввод размеров матриц
    rows_A = validate_input("Введите количество строк матрицы A: ")
    cols_A = validate_input("Введите количество столбцов матрицы A: ")
    rows_B = validate_input("Введите количество строк матрицы B: ")
    cols_B = validate_input("Введите количество столбцов матрицы B: ")

    # Проверка корректности размеров матриц
    if cols_A != rows_B:
        print("Ошибка: количество столбцов матрицы A должно совпадать с количеством строк матрицы B.")
        return

    # Генерация матриц A и B случайными числами
    A = np.random.randint(1, 10, size=(rows_A, cols_A))
    B = np.random.randint(1, 10, size=(rows_B, cols_B))
    print("Матрица A:")
    print(A)
    print("Матрица B:")
    print(B)

    # Создание пула процессов
    processes = []
    manager = mp.Manager()
    results = manager.list([None] * cols_B)

    print("\nЗапуск процессов...")
    for col_index in range(cols_B):
        delay = (col_index + 1) * 200  # Задержка t = номер_процесса * 200 мс
        args = (A, B, col_index, col_index + 1, os.getpid(), delay)  # Формируем кортеж
        process = mp.Process(target=multiply_column, args=(args,))
        processes.append(process)
        process.start()

    # Ожидание завершения всех процессов
    for process in processes:
        process.join()

    # Вывод результата
    result_matrix = np.column_stack(results)
    print("\nРезультат умножения матриц:")
    print(result_matrix)


if __name__ == "__main__":
    main()
