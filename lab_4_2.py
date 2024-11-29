import matplotlib.pyplot as plt

def measure_performance(A, B, num_threads):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(winograd_multiply, A, B) for _ in range(num_threads)]
        concurrent.futures.wait(futures)
    end_time = time.time()
    return end_time - start_time

def plot_performance(A, B):
    num_threads_list = list(range(1, 11))
    times = []
    for num_threads in num_threads_list:
        times.append(measure_performance(A, B, num_threads))

    plt.plot(num_threads_list, times, marker='o')
    plt.xlabel('Число потоков')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Зависимость времени выполнения от числа потоков')
    plt.show()

if __name__ == "__main__":
    m = 4
    n = 4
    p = 4
    A = np.random.randint(0, 10, size=(m, n))
    B = np.random.randint(0, 10, size=(n, p))

    plot_performance(A, B)
