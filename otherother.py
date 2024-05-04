import random
import time

class TennerGridCSP:
    def __init__(self, rows, columns, column_sums):
        self.rows = rows
        self.columns = columns
        self.column_sums = column_sums
        self.grid = [[-1] * columns for _ in range(rows)]
        self.unassigned_variables = [(i, j) for i in range(rows) for j in range(columns)]
        self.solution_path = []
        self.variable_assignment = 0
        self.consistency_checks = 0

    def is_valid(self, row, column, value):
        # Check if the value is not already in the same row
        if value in self.grid[row]:
            return False
        
        # Check if the value is not already in the same column and the column sum constraint is satisfied
        column_sum = sum(self.grid[i][column] for i in range(self.rows) if self.grid[i][column] != -1) + value
        if column_sum > self.column_sums[column]:
            return False
        
        # Check if the value is different from its neighbors
        neighbors = [(row-1, column), (row+1, column), (row, column-1), (row, column+1)]
        for r, c in neighbors:
            if 0 <= r < self.rows and 0 <= c < self.columns and self.grid[r][c] == value:
                return False

        return True

    def solve_simple_backtracking(self):
        if not self.unassigned_variables:
            return True

        row, column = self.unassigned_variables[0]

        for value in range(10):
            if self.is_valid(row, column, value):
                self.grid[row][column] = value
                self.variable_assignment += 1
                self.solution_path.append((row, column, value))
                self.unassigned_variables.remove((row, column))

                if self.solve_simple_backtracking():
                    return True
                else:
                    self.grid[row][column] = -1
                    self.unassigned_variables.append((row, column))
                    self.solution_path.remove((row, column, value))
        return False

    def solve_forward_checking(self):
        # TODO: Implement Forward Checking algorithm
        pass

    def solve_forward_checking_mrv(self):
        # TODO: Implement Forward Checking with MRV heuristic algorithm
        pass

    def generate_puzzle(self):
        # Randomly fill the grid with valid numbers
        for row in range(self.rows):
            for column in range(self.columns):
                valid_values = [value for value in range(10) if self.is_valid(row, column, value)]
                if valid_values:
                    self.grid[row][column] = random.choice(valid_values)
                    self.unassigned_variables.remove((row, column))

    def print_solution(self):
        print("Final CSP Tenner variable assignments:")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print("Number of variable assignments:", self.variable_assignment)
        print("Number of consistency checks:", self.consistency_checks)
        print("Solution found:")
        print("Time used to solve the problem: {} seconds".format(self.solve_time))

# Example usage
if __name__ == "__main__":
    rows = 
    columns = 10
    column_sums = [random.randint(0, 45) for _ in range(columns)]

    print("Initial state:")
    puzzle = TennerGridCSP(rows, columns, column_sums)
    puzzle.generate_puzzle()
    for row in puzzle.grid:
        print(" ".join(str(cell) for cell in row))
    print("Column sums:", column_sums)

    print("\nSolving with Simple Backtracking:")
    start_time = time.time()
    puzzle.solve_simple_backtracking()
    puzzle.solve_time = time.time() - start_time
    puzzle.print_solution()

    # Add similar sections for solving with Forward Checking and Forward Checking with MRV heuristic
