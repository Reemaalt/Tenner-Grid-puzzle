import random
import time

# Define the Tenner Grid class
class TennerGrid:
    ROWS = 3
    COLUMNS = 10

    def __init__(self):
        self.grid = None

    # Method to generate a random Tenner Grid puzzle
    @staticmethod
    def generate_grid():
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
        for col in range(self.COLUMNS):
            column_values = [self.grid[row][col] for row in range(self.ROWS) if self.grid[row][col] is not None]
            if len(column_values) != len(set(column_values)):
                return False

        # Rule 3: Numbers in the columns must add up to the given sums.
        # Assuming column_sums is an attribute of the instance
        for col in range(self.COLUMNS):
            column_sum = sum(self.grid[row][col] for row in range(self.ROWS) if self.grid[row][col] is not None)
            if column_sum != self.column_sums[col]:
                return False

        # Rule 4: Numbers in connecting cells must be different.
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                current_val = self.grid[row][col]
                # Check adjacent cells
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    new_row, new_col = row + dx, col + dy
                    # Check if new_row and new_col are within the grid bounds
                    if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLUMNS:
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

# Function to compare CSP algorithms
def compare_csp_algorithms(grid):
    algorithms = ['Simple Backtracking', 'Forward Checking', 'Forward Checking with MRV Heuristic']
    results = {}

    for algorithm in algorithms:
        start_time = time.time()
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
            # Add other metrics like number of assignments and consistency checks
        }

    return results

# Main execution
if __name__ == "__main__":
    # Create a Tenner Grid puzzle
    tenner_grid = TennerGrid()
    tenner_grid.grid = TennerGrid.generate_grid()  # Generate grid and assign it

    # Display initial state
    print("Initial State:")
    for row in tenner_grid.grid:
        print("|", " | ".join(str(cell) if cell != -1 else " " for cell in row), "|")

    # Compare CSP algorithms
    comparison_results = compare_csp_algorithms(tenner_grid)

    # Output the comparison results
    for algorithm, result in comparison_results.items():
        print("\n" + algorithm + ":")
        print("Final CSP Tenner Variable Assignments:")
        # Assuming the final state is the same as the initial state in this example
        for row in tenner_grid.grid:
            print("|", " | ".join(str(cell) if cell != -1 else " " for cell in row), "|")
        print("Number of Variable Assignments: 30")  # Placeholder value
        print("Number of Consistency Checks: 17")  # Placeholder value
        print("Solution Found (Final State):")
        for row in tenner_grid.grid:
            print("|", " | ".join(str(cell) if cell != -1 else " " for cell in row), "|")
        print("Time Used: {:.3f} seconds".format(result['time']))
