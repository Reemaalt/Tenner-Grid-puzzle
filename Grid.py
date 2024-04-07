import importlib
import time
import random
import subprocess
import statistics
from constraint import Problem


# Checking and installing packages
def install_package(package):
    subprocess.check_call(["pip", "install", package])

def check_and_install(package):
    spec = importlib.util.find_spec(package)
    if spec is None:
        print(f"The package '{package}' is not installed. Installing...")
        install_package(package)
        print(f"The package '{package}' has been successfully installed.")
    else:
        print(f"The package '{package}' is already installed.")

# List of packages to check/install
packages_to_check = ["python-constraint"]


# TennerGridCSP class
#ريما : الميثود ذي والاخيره لي بس حست الدنيا مبدأيا
class TennerGridCSP:
    def __init__(self, column_sums):    
        self.grid_size = 10
        self.grid = [[0] * self.grid_size for _ in range(10)]
        self.variables = [(i, j) for i in range(10) for j in range(self.grid_size)]
        self.column_sums = column_sums
        self.constraints = self.generate_constraints()
        self.num_variable_assignments = 0
        self.num_consistency_checks = 0
    
    def generate_constraints(self):
        constraints = {}
        # Add row constraints
        for i in range(10):
            for j in range(self.grid_size):
                for k in range(j + 1, self.grid_size):
                    constraints[((i, j), (i, k))] = self.all_different_constraint

        # Add column sum constraints
        for j in range(self.grid_size):
            constraints[[(i, j) for i in range(10)]] = self.exact_sum_constraint(self.column_sums[j])

        return constraints
    
    def all_different_constraint(self, *values):
        return len(set(values)) == len(values)
    
    def exact_sum_constraint(self, target_sum):
        def constraint(*values):
            return sum(values) == target_sum
        return constraint
#نوف
def solve_tenner_grid(problem):
    solutions = problem.getSolutions()
    return solutions
#نوره
def solve_tenner_grid_fc(problem):
    solutions = []
    problem.forwardChecking = True  # Enable forward checking
    for solution in problem.getSolutionIter():
        solutions.append(solution)
    return solutions
#نوره
def solve_tenner_grid_fc_mrv(problem):
    solutions = []
    problem.forwardChecking = True  # Enable forward checking
    problem.setHeuristicAlgorithm(lambda var, values: len(values))  # MRV heuristic
    for solution in problem.getSolutionIter():
        solutions.append(solution)
    return solutions

def compare_algorithms(problem):
    start_time = time.time()
    solutions_backtracking = solve_tenner_grid(problem)
    end_time_backtracking = time.time()
    time_backtracking = end_time_backtracking - start_time
    print("Backtracking:")
    print("Number of solutions:", len(solutions_backtracking))
    print("Time taken:", time_backtracking)

    start_time = time.time()
    solutions_fc = solve_tenner_grid_fc(problem)
    end_time_fc = time.time()
    time_fc = end_time_fc - start_time
    print("\nForward Checking:")
    print("Number of solutions:", len(solutions_fc))
    print("Time taken:", time_fc)

    start_time = time.time()
    solutions_fc_mrv = solve_tenner_grid_fc_mrv(problem)
    end_time_fc_mrv = time.time()
    time_fc_mrv = end_time_fc_mrv - start_time
    print("\nForward Checking with MRV heuristic:")
    print("Number of solutions:", len(solutions_fc_mrv))
    print("Time taken:", time_fc_mrv)

def generate_random_puzzle(column_sums):
    puzzle = TennerGridCSP(column_sums)
    for var in puzzle.variables:
        value = random.choice(puzzle.domain[var])
        puzzle.grid[var[0]][var[1]] = value
    return puzzle

def main():
    # Check and install packages if necessary
    for package in packages_to_check:
        check_and_install(package)

    # Configuration for the Tenner Grid problem
    column_sums = [[9, 7, 12, 10], [14, 10, 9, 15]]

    print(f"\nSolving 10x4 Tenner Grid Puzzles:")
    consistency_checks_backtracking = []
    consistency_checks_fc = []
    consistency_checks_fc_mrv = []

    for i in range(10):
        column_sum = random.choice(column_sums)
        puzzle = generate_random_puzzle(column_sum)
        print(f"\nPuzzle {i+1}:")
        print("Initial state:")
        print(puzzle.grid)
        
        print("\nBacktracking:")
        compare_algorithms(puzzle)
        consistency_checks_backtracking.append(puzzle.num_consistency_checks)

        print("\n=============================\n")
    
    print("\nMedian number of consistency checks (Backtracking):", statistics.median(consistency_checks_backtracking))

if __name__ == "__main__":
    main()
