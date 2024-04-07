"""
This program defines a function create_tenner_grid_problem
to set up the CSP and another function solve_tenner_grid to find solutions.
You can customize the rows, cols, and 
column_sums variables to configure the puzzle size and column sums
. The here configuration is for a 10 by 4 Tenner Grid Puzzle.
"""
#checking the packages code
import importlib.util
import subprocess

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

# Check and install packages if necessary
for package in packages_to_check:
    check_and_install(package)

#the project code
import time
from constraint import Problem, AllDifferentConstraint, ExactSumConstraint
#ريما
def create_tenner_grid_problem(rows, cols, sums):
   
    problem = Problem()

    # Add variables for each cell in the grid
    for row in range(rows):
        for col in range(cols):
            problem.addVariable((row, col), list(range(10)))

    # Add constraints for rows
    for row in range(rows):
        problem.addConstraint(AllDifferentConstraint(), [((row, col)) for col in range(cols)])

    # Add constraints for columns and column sums
    for col in range(cols):
        column = [((row, col)) for row in range(rows)]
        problem.addConstraint(AllDifferentConstraint(), column)
        problem.addConstraint(ExactSumConstraint(sums[col]), column)

    # Add constraints for diagonal cells
    for row in range(rows - 1):
        for col in range(cols - 1):
            problem.addConstraint(lambda a, b: a != b, ((row, col), (row + 1, col + 1)))

    return problem
#نوف
def solve_tenner_grid(problem):
    """
    Solve the Tenner Grid CSP problem using backtracking.

    Args:
        problem (Problem): The CSP problem instance.

    Returns:
        list: List of solutions.
    """
    solutions = problem.getSolutions()
    return solutions
#نورة
def solve_tenner_grid_fc(problem):
    """
    Solve the Tenner Grid CSP problem using forward checking.

    Args:
        problem (Problem): The CSP problem instance.

    Returns:
        list: List of solutions.
    """
    solutions = []
    problem.forwardChecking = True  # Enable forward checking
    for solution in problem.getSolutionIter():
        solutions.append(solution)
    return solutions
#نوره 
def solve_tenner_grid_fc_mrv(problem):
    """
    Solve the Tenner Grid CSP problem using forward checking with MRV heuristic.

    Args:
        problem (Problem): The CSP problem instance.

    Returns:
        list: List of solutions.
    """
    solutions = []
    problem.forwardChecking = True  # Enable forward checking
    problem.setHeuristicAlgorithm(lambda var, values: len(values))  # MRV heuristic
    for solution in problem.getSolutionIter():
        solutions.append(solution)
    return solutions

def compare_algorithms(problem):
    """
    Compare different CSP algorithms for solving the Tenner Grid problem.

    Args:
        problem (Problem): The CSP problem instance.
    """
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



def main():
    # Configuration for the Tenner Grid problem
    rows = 10
    cols = 4
    column_sums = [18, 24, 16, 22]

    # Create the Tenner Grid problem instance
    tenner_grid_problem = create_tenner_grid_problem(rows, cols, column_sums)

    # Compare different CSP algorithms for solving the problem
    compare_algorithms(tenner_grid_problem)

if __name__ == "__main__":
    main()