from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    x, y = coord
    grid[x][y] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True, user_input: bool = False
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            directions = []
            if x > 1:
                directions.append("up")
            if y < cols - 2:
                directions.append("right")

            if directions:
                direction = choice(directions)
                if direction == "up":
                    grid[x - 1][y] = " "
                elif direction == "right":
                    grid[x][y + 1] = " "
    if user_input:
        x_in = int(input("Введите строку для входа: "))
        y_in = int(input("Введите столбец для входа: "))
        x_out = int(input("Введите строку для выхода: "))
        y_out = int(input("Введите столбец для выхода: "))
    else:
        if random_exit:
            x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
            y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
            y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
        else:
            x_in, y_in = 0, cols - 2
            x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exits = [(x, y) for x, row in enumerate(grid) for y, cell in enumerate(row) if cell == "X"]
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    all_coords = []

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == k:
                all_coords.append((x, y))

    k += 1

    for x, y in all_coords:
        possible_positions = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]

        for nx, ny in possible_positions:
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                grid[nx][ny] = k

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    k = 0
    x_out, y_out = exit_coord

    while grid[x_out][y_out] == 0:
        k += 1
        grid = make_step(grid, k)

    path = [exit_coord]
    k = int(grid[x_out][y_out])
    x, y = exit_coord

    while grid[x][y] != 1 and k > 0:
        found = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == k - 1:
                path.append((nx, ny))
                x, y = nx, ny
                k -= 1
                found = True
                break

        if not found:
            return None

    path.reverse()
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    # Проверяем углы (все углы могут быть обработаны с использованием индексов)
    if (x == 0 or x == rows - 1) and (y == 0 or y == cols - 1):
        # Проверяем две соседние клетки для углов
        if grid[x + (1 if x == 0 else -1)][y] == "■" and grid[x][y + (1 if y == 0 else -1)] == "■":
            return True

    # Проверяем, если точка на границе (не угол)
    if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
        wall_count = 0
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        # Подсчитываем количество стен среди соседей
        for nx, ny in neighbors:
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "■":
                wall_count += 1

        # Если хотя бы три стены, то точка окружена
        if wall_count >= 3:
            return True

        # Если 2 стены, то проверяем, есть ли рядом пустая клетка
        if wall_count == 2:
            for nx, ny in neighbors:
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == " ":
                    return False

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)

    if len(exits) > 1:

        if any(encircled_exit(grid, exit) for exit in exits):
            return grid, None

        new_grid = deepcopy(grid)
        start_x, start_y = exits[0]
        end_x, end_y = exits[1]

        new_grid[start_x][start_y] = 1
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if new_grid[x][y] == " " or new_grid[x][y] == "X":
                    new_grid[x][y] = 0

        path = shortest_path(new_grid, (end_x, end_y))
        return new_grid, path

    if len(exits) == 1:

        return grid, exits

    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
