import time
import statistics
import random
# Define the Tenner Grid class
class TennerGrid:
    ROWS = 3  # Adjustable grid size
    COLUMNS = 10
    consistency = 0
    assignments = 0
    total_cons = 0
    total_assign = 0
    divide = 0

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.column_sums = [random.randint(0, 45) for _ in range(cols)]

    # Method to generate a random Tenner Grid puzzle
    @staticmethod
    def generate_puzzle():
        grid = [[-1 for _ in range(TennerGrid.COLUMNS)] for _ in range(TennerGrid.ROWS)]
        for i in range(TennerGrid.ROWS):
            for j in range(TennerGrid.COLUMNS):
                if random.random() < 0.5:
                    grid[i][j] = random.randint(0, 9)
        return grid

    # Method to check if the current grid is a valid state
    def is_valid_state(self):
        # Rule 1: Numbers appear only once in a row.
        for row in self.grid:
            if len(row) != len(set(row)):
                return False

        # Rule 2: Numbers may not be repeated in columns.
        for col in range(self.cols):
            column_values = [self.grid[row][col] for row in range(self.rows) if self.grid[row][col] is not None]
            if len(column_values) != len(set(column_values)):
                return False

        # Rule 3: Numbers in the columns must add up to the given sums.
        for col in range(self.cols):
            column_sum = sum(self.grid[row][col] for row in range(self.rows) if self.grid[row][col] is not None)
            if column_sum != self.column_sums[col]:
                return False

        # Rule 4: Numbers in connecting cells must be different.
        for row in range(self.rows):
            for col in range(self.cols):
                current_val = self.grid[row][col]
                # Check adjacent cells
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    new_row, new_col = row + dx, col + dy
                    # Check if new_row and new_col are within the grid bounds
                    if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                        if self.grid[new_row][new_col] == current_val:
                            return False

        # If all checks pass, the grid is valid
        return True

    # Method to solve the puzzle using backtracking
    def solve_backtracking(self):
        # A recursive function to solve the puzzle using backtracking
        def backtrack(row=0):
            # If we've reached the last row, the puzzle is solved
            if row == self.rows:
                return True
            # Try placing each number in the current row
            for num in range(self.cols):
                if self.can_place(row, num):
                    self.grid[row][num] = num
                    TennerGrid.assignments += 1
                    if self.is_valid_state():
                        if backtrack(row + 1):
                            return True
                    # Backtrack
                    self.grid[row][num] = None
            return False

        # Start the backtracking process
        return backtrack()

    # Method to solve the puzzle using forward checking
    def solve_forward_checking(self):
        # A recursive function to solve the puzzle using forward checking
        def forward_check(row=0, domain={i: set(range(self.cols)) for i in range(self.rows)}):
            # If we've reached the last row, the puzzle is solved
            if row == self.rows:
                return True
            # Try placing each number in the current row
            for num in domain[row]:
                if self.can_place(row, num):
                    self.grid[row][num] = num
                    TennerGrid.assignments += 1
                    # Update domains for forward checking
                    new_domain = self.update_domains(domain, row, num)
                    if self.is_valid_state():
                        if forward_check(row + 1, new_domain):
                            return True
                    # Backtrack
                    self.grid[row][num] = None
            return False

        # Start the forward checking process
        return forward_check()

    # Method to solve the puzzle using forward checking with MRV heuristic
    def solve_forward_checking_mrv(self):
        # A recursive function to solve the puzzle using forward checking with MRV heuristic
        def forward_check_mrv(row=0, domain={i: set(range(self.cols)) for i in range(self.rows)}):
            # If we've reached the last row, the puzzle is solved
            if row == self.rows:
                return True
            # Select the variable with the minimum remaining values (MRV)
            mrv_row = min(domain.keys(), key=lambda r: len(domain[r]))
            # Try placing each number in the MRV row
            for num in domain[mrv_row]:
                if self.can_place(mrv_row, num):
                    self.grid[mrv_row][num] = num
                    TennerGrid.assignments += 1
                    # Update domains for forward checking
                    new_domain = self.update_domains(domain, mrv_row, num)
                    if self.is_valid_state():
                        if forward_check_mrv(row + 1, new_domain):
                            return True
                    # Backtrack
                    self.grid[mrv_row][num] = None
            return False

        # Start the forward checking with MRV process
        return forward_check_mrv()

    # Helper function to check if a number can be placed in a given row and column
    def can_place(self, row, col):
        # Check if the number is not in the same row
        if col in self.grid[row]:
            return False

        # Check if the number is not in the same column
        for r in range(self.rows):
            if self.grid[r][col] == col:
                return False

        # Check if the number does not violate the column sum constraint
        column_sum = sum(self.grid[r][col] for r in range(self.rows) if self.grid[r][col] is not None)
        if column_sum + col > self.column_sums[col]:
            return False

        # Check if the number is different from adjacent cells (Rule 4)
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                if self.grid[new_row][new_col] == col:
                    return False

        # If all checks pass, the number can be placed
        return True

    # Helper function to update the domain of possible values for each row after placing a number
    def update_domains(self, domain, row, col):
        new_domain = {r: domain[r].copy() for r in domain}
        # Remove the placed number from the domain of the current row
        new_domain[row].remove(col)

        # Update the domains of the other rows
        for r in range(self.rows):
            if col in new_domain[r]:
                new_domain[r].remove(col)

        return new_domain

    @staticmethod
    def reset_counters():
        TennerGrid.divide += 1
        TennerGrid.total_cons += TennerGrid.consistency
        TennerGrid.total_assign += TennerGrid.assignments
        TennerGrid.consistency = 0
        TennerGrid.assignments = 0

    @staticmethod
    def print_grid(grid):
        print("\nFinal CSP Tenner Variable Assignments:")
        for i in range(TennerGrid.ROWS):
            print("|", end="")
            for j in range(TennerGrid.COLUMNS):
                if grid[i][j] is not None:
                    print(f" {grid[i][j]:>2} ", end="")
                else:
                    print("   ", end="")
            print("|")


    @staticmethod
    def print_initial_state(grid):
        print("\nInitial State:")
        for i in range(TennerGrid.ROWS):
            print("|", end="")
            for j in range(TennerGrid.COLUMNS):
                if grid[i][j] is not None:
                    print(f" {grid[i][j]:>2} ", end="")
                else:
                    print("   ", end="")
            print("|")


# Function to compare CSP algorithms
def compare_csp_algorithms(grid):
    algorithms = ['Simple Backtracking', 'Forward Checking', 'Forward Checking with MRV Heuristic']
    results = {}

    for algorithm in algorithms:
        start_time = time.time()
        TennerGrid.reset_counters()
        if algorithm == 'Simple Backtracking':
            grid.solve_backtracking()
        elif algorithm == 'Forward Checking':
            grid.solve_forward_checking()
        else:
            grid.solve_forward_checking_mrv()
        end_time = time.time()

        # Record the results
        results[algorithm] = {
            'time': end_time - start_time,
            'assignments': TennerGrid.assignments,
            'consistency': TennerGrid.consistency
        }

    return results

# Main execution
if __name__ == "__main__":

    # Perform comparison over five runs
    consistency_checks = {'Simple Backtracking': [], 'Forward Checking': [], 'Forward Checking with MRV Heuristic': []}
    for _ in range(5):
        # Create a Tenner Grid puzzle
        grid = TennerGrid(TennerGrid.ROWS, TennerGrid.COLUMNS)
        grid.grid = TennerGrid.generate_puzzle()

        # Compare CSP algorithms
        comparison_results = compare_csp_algorithms(grid)

        # Output the comparison results
        for algorithm, result in comparison_results.items():
            consistency_checks[algorithm].append(result['consistency'])
            TennerGrid.print_initial_state(grid.grid)
            TennerGrid.print_grid(grid.grid)
            print(f"Number of Variable Assignments ({algorithm}): {result['assignments']}")
            print(f"Number of Consistency Checks ({algorithm}): {result['consistency']}")
            print(f"Time taken ({algorithm}): {result['time']:.4f} seconds")
            print("-" * 50)

    # Output median consistency checks
    print("\nMedian Number of Consistency Checks:")
    for algorithm, checks in consistency_checks.items():
        print(f"{algorithm}: {statistics.median(checks)}")