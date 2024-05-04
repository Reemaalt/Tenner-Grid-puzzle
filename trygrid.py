import random
import time

class TennerGridCSP:
    def __init__(self, size):
        self.rows, self.columns = size
        self.grid = None
        self.generate_grid()

    def generate_grid(self):
        self.grid = [[-1 for _ in range(self.columns)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                if random.random() < 0.5:
                    self.grid[i][j] = random.randint(0, 9)

    
    def is_valid_assignment(grid, row, col, num):
        # Check row and column constraints
        for i in range(len(grid)):
            if i != row and grid[i][col] == num:
                return False
        for j in range(len(grid[0])):
            if j != col and grid[row][j] == num:
                return False
        return True

    def simple_backtracking(self, grid, row=0, col=0):
        if row == self.rows:
            return True
        next_row = row + 1 if col == self.columns - 1 else row
        next_col = (col + 1) % self.columns
        if grid[row][col] != -1:
            return self.simple_backtracking(grid, next_row, next_col)
        for num in range(10):
            if self.is_valid_assignment(grid, row, col, num):
                grid[row][col] = num
                if self.simple_backtracking(grid, next_row, next_col):
                    return True
        grid[row][col] = -1
        return False

def main():
    # Configure your program to solve 10x3, 10x4, 10x5, or 10x6 Tenner Grid Puzzles
    puzzle_size = (3, 10)  # Example: 10 rows, 3 columns

    # Run solvers and collect statistics
    for _ in range(5):  # Repeat for statistical analysis
        csp = TennerGridCSP(puzzle_size)
        
        # Generate a random puzzle
        print("Random Puzzle:")
        for row in csp.grid:
            print(row)

        # Record starting time
        start_time = time.time()

        # Run simple backtracking solver
        grid_copy = [row[:] for row in csp.grid]
        if csp.simple_backtracking(grid_copy):
            print("\nSolution Found:")
            for row in grid_copy:
                print(row)
        else:
            print("\nNo Solution Found")

        # Record ending time
        end_time = time.time()

        # Record statistics: time taken
        print("Time taken:", end_time - start_time)

if __name__ == "__main__":
    main()

