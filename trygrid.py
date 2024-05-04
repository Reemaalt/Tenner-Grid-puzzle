import random
import time

class TennerGridSolver:
    def __init__(self, grid_size=(3, 10)):
        self.grid_size = grid_size
        self.grid = [[0] * grid_size[1] for _ in range(grid_size[0])]
        self.row_constraints = [0] * grid_size[0]
        self.col_constraints = [0] * grid_size[1]
        self.variable_assignments = 0
        self.consistency_checks = 0

    def solve(self):
        start_time = time.time()
        solution = self.backtrack_search()
        end_time = time.time()
        time_taken = end_time - start_time
        return solution, time_taken

    def backtrack_search(self):
        assignment = {}
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        if len(assignment) == self.grid_size[0] * self.grid_size[1]:
            return assignment

        row, col = self.select_unassigned_variable(assignment)
        remaining_values = self.get_remaining_values(row, col, assignment)
        for value in remaining_values:
            self.consistency_checks += 1
            if self.is_valid_assignment(row, col, value):
                assignment[(row, col)] = value
                self.variable_assignments += 1
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[(row, col)]
        return None

    def select_unassigned_variable(self, assignment):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if (i, j) not in assignment:
                    return i, j
        return -1, -1  # Grid is complete

    def is_valid_assignment(self, row, col, value):
        self.consistency_checks += 1
        if value in self.grid[row]:
            return False

        if self.row_constraints[row] != 0:
            if sum(self.grid[row]) + value > self.row_constraints[row]:
                return False

        if self.col_constraints[col] != 0:
            col_sum = sum(self.grid[i][col] for i in range(self.grid_size[0]) if self.grid[i][col] >= 0)
            if col_sum + value > self.col_constraints[col]:
                return False

        if not self.check_adjacent_cells(row, col, value):
            return False

        return True

    def check_adjacent_cells(self, row, col, value):
        adjacent_positions = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1),                     (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
        ]
        for r, c in adjacent_positions:
            if 0 <= r < self.grid_size[0] and 0 <= c < self.grid_size[1]:
                if self.grid[r][c] == value:
                    return False
        return True

    def generate_random_grid(self, max_attempts=10):
        for _ in range(max_attempts):
            # Generate a random grid with random numbers
            for i in range(self.grid_size[0]):
                for j in range(self.grid_size[1]):
                    # Introduce randomness by setting some cells to 0
                    self.grid[i][j] = random.randint(0, 9)

            # Set column sums to random values
            self.col_constraints = [random.randint(0, 45) for _ in range(self.grid_size[1])]

            


    def is_solvable(self):
        for j in range(self.grid_size[1]):
            col_sum = sum(self.grid[i][j] for i in range(self.grid_size[0]) if self.grid[i][j] >= 0)
            if self.col_constraints[j] != 0 and col_sum != self.col_constraints[j]:
                return False
        return True

    def get_remaining_values(self, row, col, assignment):
        remaining_values = set(range(10))
        for r in range(self.grid_size[0]):
            for c in range(self.grid_size[1]):
                if (r, c) in assignment:
                    remaining_values.discard(assignment[(r, c)])
        return remaining_values

    def print_grid(self, message=""):
        if message:
            print(message)
        for row in self.grid:
            print(row)

    def print_solution_info(self, time_taken):
        print("\nFinal CSP Tenner Variable Assignments:")
        self.print_grid()
        print("\nNumber of Variable Assignments:", self.variable_assignments)
        print("Number of Consistency Checks:", self.consistency_checks)
        print("\nTime Used to Solve the Problem:", time_taken)

# Example usage:
if __name__ == "__main__":
    puzzle = TennerGridSolver(grid_size=(3, 10))
    # Adjusting constraints according to Tenner Grids math puzzles rules
    puzzle.row_constraints = [10, 15, 12]  # Example row sums

    print("Randomly generated unsolved grid:")
    puzzle.generate_random_grid()
    puzzle.print_grid()

    print("\nSolving the puzzle...")
    solution, time_taken = puzzle.solve()
    if solution:
        print("\nSolution:")
        puzzle.print_solution_info(time_taken)
    else:
        print("No solution exists.")
