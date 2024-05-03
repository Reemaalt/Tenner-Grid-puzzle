import random
import copy
import time

class TennerGridSolver:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[-1]*width for _ in range(height)]  # Initialize empty grid
        self.column_sums = [0]*width  # Initialize column sums
        self.constraints = set()

    def generate_puzzle(self):
        for j in range(self.width):
            column_sum = random.randint(0, 45)  # Random sum for each column
            self.column_sums[j] = column_sum
            self.constraints.add((j, column_sum))
        self.solve_backtracking()  # Solve using backtracking to generate initial state

    def print_grid(self):
        for row in self.grid:
            print(row)

    def is_valid(self, row, col, num):
        # Check row constraint
        if num in self.grid[row]:
            return False

        # Check column sum constraint
        if sum(self.grid[i][col] for i in range(row + 1)) > self.column_sums[col]:
            return False

        # Check diagonal constraint
        if row > 0 and col > 0 and self.grid[row-1][col-1] == num:
            return False

        return True

    def solve_backtracking(self):
        self.backtracking(0, 0)

    def backtracking(self, row, col):
        if row == self.height:
            return True

        for num in range(10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                next_row = row + 1 if col == self.width - 1 else row
                next_col = col + 1 if col < self.width - 1 else 0
                if self.backtracking(next_row, next_col):
                    return True
                self.grid[row][col] = -1  # Backtrack
        return False

    def solve_forward_checking(self):
        self.forward_checking(0, 0, set())

    def forward_checking(self, row, col, assigned):
        if row == self.height:
            return True

        for num in range(10):
            if num not in assigned and self.is_valid(row, col, num):
                self.grid[row][col] = num
                next_row = row + 1 if col == self.width - 1 else row
                next_col = col + 1 if col < self.width - 1 else 0
                assigned.add(num)
                if self.forward_checking(next_row, next_col, assigned):
                    return True
                assigned.remove(num)
                self.grid[row][col] = -1  # Backtrack
        return False

    def solve_forward_checking_mrv(self):
        self.forward_checking_mrv(0, 0, set())

    def forward_checking_mrv(self, row, col, assigned):
        if row == self.height:
            return True

        unassigned_vars = [(r, c) for r in range(row, self.height) for c in range(self.width) if self.grid[r][c] == -1]
        unassigned_vars.sort(key=lambda var: len([(r, c) for r, c in self.constraints if r == var[1] and c > var[0]]))

        for var_row, var_col in unassigned_vars:
            for num in range(10):
                if num not in assigned and self.is_valid(var_row, var_col, num):
                    self.grid[var_row][var_col] = num
                    assigned.add(num)
                    if self.forward_checking_mrv(row, col, assigned):
                        return True
                    assigned.remove(num)
                    self.grid[var_row][var_col] = -1  # Backtrack
        return False

def main():
    width = 10
    height = 3
    solver = TennerGridSolver(width, height)
    solver.generate_puzzle()
    print("Initial state:")
    solver.print_grid()
    print("\nSolving using Backtracking:")
    start_time = time.time()
    solver.solve_backtracking()
    end_time = time.time()
    print("Time taken to solve (Backtracking):", end_time - start_time, "seconds")
    print("\nFinal state:")
    solver.print_grid()

    solver = TennerGridSolver(width, height)
    solver.generate_puzzle()
    print("\nSolving using Forward Checking:")
    start_time = time.time()
    solver.solve_forward_checking()
    end_time = time.time()
    print("Time taken to solve (Forward Checking):", end_time - start_time, "seconds")
    print("\nFinal state:")
    solver.print_grid()

    solver = TennerGridSolver(width, height)
    solver.generate_puzzle()
    print("\nSolving using Forward Checking with MRV:")
    start_time = time.time()
    solver.solve_forward_checking_mrv()
    end_time = time.time()
    print("Time taken to solve (Forward Checking + MRV):", end_time - start_time, "seconds")
    print("\nFinal state:")
    solver.print_grid()

if __name__ == "__main__":
    main()
