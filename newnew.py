import numpy as np

class TennerGridCSP:
    def __init__(self, grid_size, row_sums, col_sums):
        self.grid_size = grid_size
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        self.variables = [(i, j) for i in range(grid_size) for j in range(grid_size)]
        self.domains = {variable: set(range(1, 10)) for variable in self.variables}
        self.constraints = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def check_constraint(self, variable, value):
        for constraint in self.constraints:
            if not constraint(self.grid, variable, value):
                return False
        return True

    def solve(self):
        if self.is_complete():
            return self.grid
        variable = self.select_unassigned_variable()
        for value in self.order_domain_values(variable):
            if self.check_constraint(variable, value):
                self.grid[variable] = value
                result = self.solve()
                if result is not None:
                    return result
                self.grid[variable] = 0  # Backtrack
        return None

    def is_complete(self):
        return np.all(self.grid != 0)

    def select_unassigned_variable(self):
        for variable in self.variables:
            if self.grid[variable] == 0:
                return variable

    def order_domain_values(self, variable):
        return sorted(self.domains[variable])

def row_constraint(grid, variable, value):
    row, col = variable
    return value not in grid[row, :]

def col_constraint(grid, variable, value):
    row, col = variable
    return value not in grid[:, col]

def sum_constraint(grid, variable, value):
    row, col = variable
    return sum(grid[:, col]) <= col_sums[col] and sum(grid[row, :]) <= row_sums[row]

def diff_constraint(grid, variable, value):
    row, col = variable
    neighbors = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]
    for r, c in neighbors:
        if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
            if grid[r, c] == value:
                return False
    return True

# Define the puzzle parameters
grid_size = 10
row_sums = [sum(range(1, grid_size + 1))] * grid_size
col_sums = [sum(range(1, grid_size + 1))] * grid_size

# Create the CSP instance
tenner_grid = TennerGridCSP(grid_size, row_sums, col_sums)

# Add constraints
for row in range(grid_size):
    for col in range(grid_size):
        tenner_grid.add_constraint(row_constraint)
        tenner_grid.add_constraint(col_constraint)
        tenner_grid.add_constraint(sum_constraint)
        tenner_grid.add_constraint(diff_constraint)

# Solve the puzzle
solution = tenner_grid.solve()
print(solution)
