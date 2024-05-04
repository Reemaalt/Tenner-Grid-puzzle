import random
import time

# Define the Tenner Grid class
class TennerGrid:
    ROWS = 3
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
        # Implement backtracking algorithm here
        pass

    # Method to solve the puzzle using forward checking
    def solve_forward_checking(self):
        # Implement forward checking algorithm here
        pass

    # Method to solve the puzzle using forward checking with MRV heuristic
    def solve_forward_checking_mrv(self):
        # Implement forward checking with MRV heuristic here
        pass
    
    def reset_counters():
        TennerGrid.divide += 1
        TennerGrid.total_cons += TennerGrid.consistency
        TennerGrid.total_assign += TennerGrid.assignments
        TennerGrid.consistency = 0
        TennerGrid.assignments = 0

    @staticmethod
    def print_grid(grid):
        print("\n---------Final State---------")
        for i in range(TennerGrid.ROWS):
            print("|", end="")
            for j in range(TennerGrid.COLUMNS):
                print(f"{grid[i][j]:>2} ", end="")
            print("|")
        print("------------------------------\n")

    @staticmethod
    def print_initial_state(grid):
        print("\n--------Initial State---------")
        for i in range(TennerGrid.ROWS):
            print("|", end="")
            for j in range(TennerGrid.COLUMNS):
                if grid[i][j] != -1:
                    print(f"{grid[i][j]:>2} ", end="")
                else:
                    print("   ", end="")
            print("|")
        print("------------------------------")

# Function to compare CSP algorithms
def compare_csp_algorithms(grid):
    algorithms = ['Backtracking', 'Forward Checking', 'FC+MRV']
    results = {}

    for algorithm in algorithms:
        start_time = time.time()
        if algorithm == 'Backtracking':
            grid.solve_backtracking()
        elif algorithm == 'Forward Checking':
            grid.solve_forward_checking()
        else:
            grid.solve_forward_checking_mrv()
        end_time = time.time()

        # Record the results
        results[algorithm] = {
            'time': end_time - start_time,
            # Add other metrics like number of assignments and consistency checks
        }

    return results




# Main execution
if __name__ == "__main__":

    # Create a Tenner Grid puzzle
    grid = TennerGrid(TennerGrid.ROWS, TennerGrid.COLUMNS)
    grid.grid = TennerGrid.generate_puzzle()
    TennerGrid.print_initial_state(grid.grid)

    # Compare CSP algorithms
    comparison_results = compare_csp_algorithms(grid)
    
    print("consistency:", TennerGrid.consistency)
    print("assignments:", TennerGrid.assignments)
    TennerGrid.reset_counters()

    print("average consistency:", (TennerGrid.total_cons / TennerGrid.divide))
    print("average assignments:", (TennerGrid.total_assign / TennerGrid.divide))


    # Output the comparison results
    print("\nComparison Results:")
    for algorithm, result in comparison_results.items():
        print(f"{algorithm}: Time taken - {result['time']} seconds")
