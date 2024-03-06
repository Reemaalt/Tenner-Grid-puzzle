"""
a Constraint Satisfaction Problem (CSP). In this case, the constraints involve 
ensuring that numbers don't repeat in rows, the column sums match the given targets,
and adjacent cells have different digits. 
the constraint-satisfaction library python-constraint. 
 You can install it using:
 
 pip install python-constraint
"""

"""
This program defines a function create_tenner_grid_problem
to set up the CSP and another function solve_tenner_grid to find solutions.
You can customize the rows, cols, and 
column_sums variables to configure the puzzle size and column sums
. The here configuration is for a 10 by 4 Tenner Grid Puzzle.
"""
# extend and modify the code to include additional heuristics

from constraint import Problem, AllDifferentConstraint, ExactSumConstraint

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

def solve_tenner_grid(problem):
    solutions = problem.getSolutions()
    return solutions

# Example configuration: 10 by 4 Tenner Grid Puzzle
rows = 10
cols = 4
column_sums = [18, 24, 16, 22]

tenner_grid_problem = create_tenner_grid_problem(rows, cols, column_sums)
solutions = solve_tenner_grid(tenner_grid_problem)

# Print the first solution
if solutions:
    solution = solutions[0]
    for row in range(rows):
        print([solution[(row, col)] for col in range(cols)])
else:
    print("No solution found.")
