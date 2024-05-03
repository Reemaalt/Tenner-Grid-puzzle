#These lines import necessary modules 
import random
import time
from copy import deepcopy

#class represents the Tenner Grid CSP (Constraint Satisfaction Problem).
class TennerGridCSP:
     # methods for initializing the CSP, generating constraints, checking consistency and selecting variables
    def __init__(self, grid_size):
     # Constructor to initialize the Tenner Grid CSP
        self.grid_size = grid_size
        self.grid = [[random.randint(0, 9) for _ in range(grid_size)] for _ in range(10)]  # Initialize grid
        self.variables = [(i, j) for i in range(10) for j in range(grid_size)]  # List of variables
        self.domain = {var: list(range(1, 11)) for var in self.variables}  # Domain of each variable
        self.constraints = self.generate_constraints()  # Generate constraints
        self.num_variable_assignments = 0  # Counter for variable assignments
        self.num_consistency_checks = 0  # Counter for consistency checks
          
          

    def generate_constraints(self):
        # Method to generate constraints for the CSP
        constraints = {}
        for i in range(10):
            for j in range(self.grid_size - 1):
                for k in range(j + 1, self.grid_size):
                    var1 = (i, j)
                    var2 = (i, k)
                    if (var1, var2) not in constraints:
                        constraints[(var1, var2)] = []
                    for val1 in range(1, 11):
                        for val2 in range(1, 11):
                            if val1 != val2:
                                constraints[(var1, var2)].append((val1, val2))
        return constraints
    
    
    def is_consistent(self, var, value, assignment):
            # Method to check consistency of a variable assignment
            for other_var in assignment:
                if other_var != var and (other_var, var) in self.constraints:
                    if (assignment[other_var], value) not in self.constraints[(other_var, var)]:
                        self.num_consistency_checks += 1  # Increment consistency check counter
                        return False
            return True

    def select_unassigned_variable(self, assignment):
        # Method to select an unassigned variable
        unassigned = [(var, len(self.domain[var])) for var in self.variables if var not in assignment]
        return min(unassigned, key=lambda x: x[1])[0]

    #algorithms to solve like backtracking, forward checking, and forward checking with MRV.
    def backtracking_search(self):
        # Method implementing backtracking search algorithm
        return self.backtrack({}, self.domain)
    
    def backtrack(self, assignment, remaining):
        # Recursive method for backtracking
        if len(assignment) == len(self.variables):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in remaining[var]:
            self.num_variable_assignments += 1
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment, remaining)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def forward_checking(self):
        # Method implementing forward checking algorithm
        return self.forward_check({}, deepcopy(self.domain))

    def forward_check(self, assignment, remaining):
        # Recursive method for forward checking
        if len(assignment) == len(self.variables):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in remaining[var][:]:
            self.num_variable_assignments += 1
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                pruned = False
                for neighbor in self.variables:
                    if neighbor != var and (neighbor, var) in self.constraints:
                        for neighbor_value in remaining[neighbor][:]:
                            if (value, neighbor_value) not in self.constraints[(neighbor, var)]:
                                remaining[neighbor].remove(neighbor_value)
                                self.num_consistency_checks += 1
                                pruned = True
                    if not remaining[neighbor]:
                        del assignment[var]
                        return None
                if not pruned:
                    result = self.forward_check(assignment, remaining)
                    if result is not None:
                        return result
                del assignment[var]
                for neighbor in self.variables:
                    if neighbor != var and (neighbor, var) in self.constraints:
                        remaining[neighbor] = self.domain[neighbor][:]
        return None

    def forward_checking_mrv(self):
        # Method implementing forward checking with MRV (Minimum Remaining Values) algorithm
        return self.forward_check_mrv({}, deepcopy(self.domain))

    def forward_check_mrv(self, assignment, remaining):
        # Recursive method for forward checking with MRV
        if len(assignment) == len(self.variables):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in sorted(remaining[var], key=lambda x: self.calculate_remaining_values(var, x, assignment)):
            self.num_variable_assignments += 1
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                pruned = False
                for neighbor in self.variables:
                    if neighbor != var and (neighbor, var) in self.constraints:
                        for neighbor_value in remaining[neighbor][:]:
                            if (value, neighbor_value) not in self.constraints[(neighbor, var)]:
                                remaining[neighbor].remove(neighbor_value)
                                self.num_consistency_checks += 1
                                pruned = True
                    if not remaining[neighbor]:
                        del assignment[var]
                        return None
                if not pruned:
                    result = self.forward_check_mrv(assignment, remaining)
                    if result is not None:
                        return result
                del assignment[var]
                for neighbor in self.variables:
                    if neighbor != var and (neighbor, var) in self.constraints:
                        remaining[neighbor] = self.domain[neighbor][:]
        return None

    # helper methods
    def calculate_remaining_values(self, var, value, assignment):
        # Method to calculate remaining values for a variable ,helps in forward checking with MRV
        count = 0
        for neighbor in self.variables:
            if neighbor != var and (neighbor, var) in self.constraints:
                for neighbor_value in self.domain[neighbor]:
                    if (value, neighbor_value) in self.constraints[(neighbor, var)] and neighbor not in assignment:
                        count += 1
        return count
    
    def display_grid(self):
        # Method to display the grid
        for row in self.grid:
            print(row)



import random

def generate_random_puzzle(grid_size):
    # Function to generate a random unsolved puzzle
    puzzle = TennerGridCSP(grid_size)
    
    # Initialize the grid with random numbers and empty cells indicated by -1
    for var in puzzle.variables:
        puzzle.grid[var[0]][var[1]] = random.randint(-1, 10)
    
    # Calculate the sum for each column and assign it to the bottom cell
    for j in range(grid_size):
        column_sum = sum(puzzle.grid[i][j] for i in range(10) if puzzle.grid[i][j] != -1)
        puzzle.grid[9][j] = column_sum
    
    return puzzle


def main():

    grid_sizes = [10]  # Adjusted for 10x3 Tenner Grid Puzzles
    algorithms = {
        "Simple Backtracking": TennerGridCSP.backtracking_search,
        "Forward Checking": TennerGridCSP.forward_checking,
        "Forward Checking with MRV": TennerGridCSP.forward_checking_mrv
    }

    for grid_size in grid_sizes:
        print(f"Solving 10x{grid_size} Tenner Grid Puzzle")
        print("-" * 40)

        for alg_name, algorithm in algorithms.items():
            print(f"Using {alg_name}:")
            print("-" * 40)

            consistency_checks = []
            variable_assignments = []
            start_time = time.time()

            for _ in range(5):  # Run each algorithm 5 times and calculate median
                puzzle = generate_random_puzzle(grid_size)
                if algorithm.__name__ == "backtracking_search":
                    solution = algorithm(puzzle)
                else:
                    solution = algorithm(puzzle)

                consistency_checks.append(puzzle.num_consistency_checks)
                variable_assignments.append(puzzle.num_variable_assignments)
               
                print("Initial State:")
                puzzle.display_grid()
                print("Solution found in", round(time.time() - start_time, 3), "seconds.")
                print("Number of Variable Assignments:", puzzle.num_variable_assignments)
                print("Number of Consistency Checks:", puzzle.num_consistency_checks)
                print("Final CSP Tenner Variable Assignments:") 
        
                for i in range(10):
                  row_values = [solution[(i, j)] for j in range(grid_size)]
                  print(row_values)
                print("-" * 40)

            median_consistency_checks = sorted(consistency_checks)[len(consistency_checks) // 2]
            median_variable_assignments = sorted(variable_assignments)[len(variable_assignments) // 2]
            print("Median Number of Consistency Checks:", median_consistency_checks)
            print("Median Number of Variable Assignments:", median_variable_assignments)
            print("\n")

if __name__ == "__main__":
    main()
 
""""Alright, let's break it down:

Puzzle Representation:

Imagine a game where you have a grid of 10 rows and 3 columns (but it can be adjusted).
Each cell in this grid can hold a number from 1 to 10.
Goal:

The goal is to fill in each cell of the grid with a number from 1 to 10 in such a way that certain rules are satisfied.
Rules:

The numbers in each row must be unique (no repeating numbers within a row).
Certain pairs of neighboring cells must have their numbers in a specific relationship, like one being greater than the other.
How the Program Solves the Puzzle:

The program tries different strategies to find a solution to the puzzle.
It has three main strategies: simple backtracking, forward checking, and forward checking with MRV (which is a more efficient version).
These strategies work by guessing numbers for the cells, checking if the guesses follow the rules, and adjusting if they don't until a solution is found.
What the Program Does:

It first creates a random puzzle grid.
Then, it tries each solving strategy multiple times to see which one works best.
It measures how many times it needs to check if the guesses follow the rules (consistency checks) and how many guesses it needs to make (variable assignments).
Finally, it prints out the median (middle value) of these measurements to give an idea of how efficient each strategy is.
The Output:

After trying each strategy multiple times, the program shows which strategy worked best and how many consistency checks and variable assignments were needed on average to solve the puzzle.
In simple terms, the program is like a smart kid trying different ways to solve a puzzle and figuring out which way is the fastest and most efficient."""
