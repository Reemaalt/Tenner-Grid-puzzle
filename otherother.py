import random

class BacktrackingMRV:
    ROWS = 4
    COLUMNS = 10
    consistency = 0
    assignments = 0
    total_cons = 0
    total_assign = 0
    divide = 0

    @staticmethod
    def backtrack_mrv(grid, row, col):
        if row == BacktrackingMRV.ROWS - 1 and col == BacktrackingMRV.COLUMNS:
            return True
        if col == BacktrackingMRV.COLUMNS:
            row += 1
            col = 0
        if grid[row][col] != -1:
            return BacktrackingMRV.backtrack_mrv(grid, row, col + 1)
        min_remaining_values = 10000
        min_row = -1
        min_col = -1
        for i in range(BacktrackingMRV.ROWS - 1):
            for j in range(BacktrackingMRV.COLUMNS):
                if grid[i][j] == -1:
                    remaining_values = BacktrackingMRV.get_remaining_values(grid, i, j)
                    if remaining_values < min_remaining_values:
                        min_remaining_values = remaining_values
                        min_row = i
                        min_col = j
        for num in range(10):
            if BacktrackingMRV.is_safe(grid, min_row, min_col, num):
                grid[min_row][min_col] = num
                BacktrackingMRV.assignments += 1
                if BacktrackingMRV.backtrack_mrv(grid, 0, 0):
                    return True
        grid[min_row][min_col] = -1
        BacktrackingMRV.assignments += 1
        return False

    @staticmethod
    def get_remaining_values(grid, row, col):
        remaining_values = 0
        for num in range(10):
            if BacktrackingMRV.is_safe(grid, row, col, num):
                remaining_values += 1
        return remaining_values

    @staticmethod
    def is_safe(grid, row, col, num):
        for x in range(BacktrackingMRV.COLUMNS):
            BacktrackingMRV.consistency += 1
            if grid[row][x] == num:
                return False
        for offset in [-1, 1]:
            if 0 <= row + offset < BacktrackingMRV.ROWS:
                BacktrackingMRV.consistency += 1
                if grid[row + offset][col] == num:
                    return False
        for offset in [-1, 1]:
            if 0 <= col + offset < BacktrackingMRV.COLUMNS:
                BacktrackingMRV.consistency += 1
                if grid[row][col + offset] == num:
                    return False
        sum_ = 0
        for i in range(BacktrackingMRV.ROWS - 1):
            if grid[i][col] != -1:
                sum_ += grid[i][col]
        sum_ += num
        BacktrackingMRV.consistency += 1
        return sum_ <= grid[BacktrackingMRV.ROWS - 1][col]

    @staticmethod
    def reset_counters():
        BacktrackingMRV.divide += 1
        BacktrackingMRV.total_cons += BacktrackingMRV.consistency
        BacktrackingMRV.total_assign += BacktrackingMRV.assignments
        BacktrackingMRV.consistency = 0
        BacktrackingMRV.assignments = 0

    @staticmethod
    def print_grid(grid):
        print("\n ---------Final State---------")
        for i in range(BacktrackingMRV.ROWS):
            print("|", end="")
            for j in range(BacktrackingMRV.COLUMNS):
                print(f"{grid[i][j]:2}", end=" ")
            print("|")
        print(" ------------------------------")

    @staticmethod
    def print_initial_state(grid):
        print("\n --------Initial State---------")
        for i in range(BacktrackingMRV.ROWS):
            print("|", end="")
            for j in range(BacktrackingMRV.COLUMNS):
                if grid[i][j] != -1:
                    print(f"{grid[i][j]:2}", end=" ")
                else:
                    print(f"{' ':2}", end=" ")
            print("|")
        print(" ------------------------------")

    @staticmethod
    def solve_all_grids():
        grids = [
            [[-1, 6, 2, 0, -1, -1, -1, 8, 5, 7], [-1, 0, 1, 7, 8, -1, -1, -1, 9, -1],
             [-1, 4, -1, -1, 2, -1, 3, 7, -1, 8], [13, 10, 8, 7, 19, 16, 11, 19, 15, 17]],
            [[-1, -1, 5, 3, -1, -1, 6, -1, -1, -1], [0, 7, -1, 4, 6, 5, -1, -1, 1, 3],
             [-1, 2, 3, 7, -1, 4, -1, 6, 5, -1], [10, 13, 17, 14, 8, 16, 14, 17, 14, 12]],
            [[4, -1, -1, -1, 2, 0, -1, 1, -1, 9], [7, -1, -1, 5, -1, -1, -1, 2, -1, 6],
             [4, -1, -1, 9, 7, -1, -1, -1, -1, 3], [15, 11, 10, 20, 17, 4, 23, 3, 14, 18]],
            [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, 4, -1, -1, -1, 9, -1, -1, 2, -1],
             [-1, 1, 9, 5, 8, 4, -1, 7, 6, 3], [13, 14, 20, 13, 13, 18, 10, 14, 12, 8]],
            [[5, 7, -1, 0, -1, 1, -1, -1, -1, -1], [1, -1, -1, 6, 7, -1, -1, 5, 4, -1],
             [-1, -1, -1, -1, -1, -1, 1, 7, 2, -1], [14, 12, 17, 15, 19, 10, 14, 18, 9, 7]]
        ]

        for idx, grid in enumerate(grids, start=1):
            BacktrackingMRV.print_initial_state(grid)
            if BacktrackingMRV.backtrack_mrv(grid, 0, 0):
                BacktrackingMRV.print_grid(grid)
            else:
                print("No Solution exists")
            print("consistency:", BacktrackingMRV.consistency)
            print("assignments:", BacktrackingMRV.assignments)
            BacktrackingMRV.reset_counters()

        print("average consistency:", BacktrackingMRV.total_cons / BacktrackingMRV.divide)
        print("average assignments:", BacktrackingMRV.total_assign / BacktrackingMRV.divide)


def generate_random_grid():
    # Generate an empty grid
    empty_grid = [[-1 for _ in range(BacktrackingMRV.COLUMNS)] for _ in range(BacktrackingMRV.ROWS - 1)]
    filled_grid = empty_grid.copy()

    # Fill each row randomly
    for row in range(BacktrackingMRV.ROWS - 1):
        filled_grid[row] = random.sample(range(10), k=BacktrackingMRV.COLUMNS)

    # Check and fill the last row to make it a valid Sudoku puzzle
    for col in range(BacktrackingMRV.COLUMNS):
        # Get the numbers present in the column
        column_numbers = [filled_grid[row][col] for row in range(BacktrackingMRV.ROWS - 1) if filled_grid[row][col] != -1]
        # Get the missing numbers
        missing_numbers = list(set(range(10)) - set(column_numbers))
        # Fill the missing numbers randomly
        random.shuffle(missing_numbers)
        for row in range(BacktrackingMRV.ROWS - 1):
            if filled_grid[row][col] == -1:
                filled_grid[row][col] = missing_numbers.pop()

    # Add the sum row
    for col in range(BacktrackingMRV.COLUMNS):
        filled_grid[-1][col] = sum(filled_grid[row][col] for row in range(BacktrackingMRV.ROWS - 1))

    return filled_grid


def main():
    BacktrackingMRV.solve_all_grids()

    # Randomize and solve a grid
    random_grid = generate_random_grid()
    BacktrackingMRV.print_initial_state(random_grid)
    if BacktrackingMRV.backtrack_mrv(random_grid, 0, 0):
        BacktrackingMRV.print_grid(random_grid)
    else:
        print("No Solution exists")
    print("consistency:", BacktrackingMRV.consistency)
    print("assignments:", BacktrackingMRV.assignments)
    BacktrackingMRV.reset_counters()


if __name__ == "__main__":
    main()
