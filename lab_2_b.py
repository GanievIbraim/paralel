import numpy as np

def create_grid(rows, cols):
    """Создание 2-мерной решетки"""
    grid = np.arange(rows * cols).reshape(rows, cols)
    return grid

def get_neighbors(grid, row, col):
    """Получение соседей для узла"""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:  # Верхний сосед
        neighbors.append((row - 1, col))
    if row < rows - 1:  # Нижний сосед
        neighbors.append((row + 1, col))
    if col > 0:  # Левый сосед
        neighbors.append((row, col - 1))
    if col < cols - 1:  # Правый сосед
        neighbors.append((row, col + 1))
    return neighbors

def simulate_data_transfer(grid):
    """Симуляция передачи данных между узлами"""
    rows, cols = grid.shape
    data = {tuple([i, j]): grid[i, j] for i in range(rows) for j in range(cols)}
    print("Исходные данные узлов:")
    print(data)
    
    # Передача данных каждому соседу
    transfers = {}
    for row in range(rows):
        for col in range(cols):
            node = (row, col)
            neighbors = get_neighbors(grid, row, col)
            transfers[node] = {neighbor: data[neighbor] for neighbor in neighbors}
    
    print("\nДанные, полученные каждым узлом от соседей:")
    for node, received_data in transfers.items():
        print(f"Узел {node} получил: {received_data}")

# Пример использования
if __name__ == "__main__":
    rows, cols = 4, 4
    grid = create_grid(rows, cols)
    print("Сетка:")
    print(grid)
    
    simulate_data_transfer(grid)
