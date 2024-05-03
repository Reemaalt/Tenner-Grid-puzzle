import random
import time

class TennerGridCSP:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[0] * grid_size for _ in range(10)]  # Initialize grid
        self.variables = [(i, j) for i in range(10) for j in range(grid_size)]  # List of variables
        self.domain = {var: list(range(1, 11)) for var in self.variables}  # Domain of each variable
        self.constraints = self.generate_constraints()  # Generate constraints
        self.num_variable_assignments = 1  # Counter for variable assignments
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

    def backtracking_search(self, assignment={}):
        # Method for solving CSP using backtracking search
        if len(assignment) == len(self.variables):
            return assignment  # If all variables are assigned, return assignment
        var = self.select_unassigned_variable(assignment)  # Select an unassigned variable
        for value in self.domain[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value  # Assign the value to the variable
                self.num_variable_assignments += 1  # Increment assignment counter
                result = self.backtracking_search(assignment.copy())  # Recursively search
                if result is not None:
                    return result  # If solution found, return it
                del assignment[var]  # Remove variable from assignment if no solution found
        return None  # If no solution found, return None

    def forward_checking(self, assignment):
        # Method to solve CSP using forward checking
        # Implementation similar to backtracking, with additional constraint propagation
        if len(assignment) == len(self.variables):
            return assignment  # If all variables are assigned, return assignment
        var = self.select_unassigned_variable(assignment)  # Select an unassigned variable
        for value in self.domain[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value  # Assign the value to the variable
                self.num_variable_assignments += 1  # Increment assignment counter
                inferences = self.propagate_forward_checking(var, value, assignment)
                if inferences is not None:
                    result = self.forward_checking(assignment.copy())
                    if result is not None:
                        return result  # If solution found, return it
                self.undo_inferences(inferences, assignment)  # Undo inferences
                del assignment[var]  # Remove variable from assignment if no solution found
        return None  # If no solution found, return None

    def propagate_forward_checking(self, var, value, assignment):
        # Method to perform constraint propagation (forward checking)
        inferences = {}
        for neighbor_var in self.variables:
            if neighbor_var != var and neighbor_var not in assignment:
                if (neighbor_var, var) in self.constraints:
                    for neighbor_value in self.domain[neighbor_var][:]:
                        if (neighbor_value, value) not in self.constraints[(neighbor_var, var)]:
                            self.num_consistency_checks += 1
                            self.domain[neighbor_var].remove(neighbor_value)
                            if len(self.domain[neighbor_var]) == 0:
                                # Inconsistency detected
                                self.restore_domain(inferences)
                                return None
                            inferences[neighbor_var] = neighbor_value
        return inferences

    def undo_inferences(self, inferences, assignment):
        # Method to undo inferences during backtracking
        for var, value in inferences.items():
            self.domain[var].append(value)
            del assignment[var]

    def restore_domain(self, inferences):
        # Method to restore domain during backtracking
        for var, value in inferences.items():
            self.domain[var].append(value)

    def forward_checking_mrv(self, assignment):
        # Method to solve CSP using forward checking with MRV heuristic
        if len(assignment) == len(self.variables):
            return assignment  # If all variables are assigned, return assignment
        var = self.select_unassigned_variable(assignment)  # Select an unassigned variable
        for value in self.domain[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value  # Assign the value to the variable
                self.num_variable_assignments += 1  # Increment assignment counter
                inferences = self.propagate_forward_checking(var, value, assignment)
                if inferences is not None:
                    result = self.forward_checking_mrv(assignment.copy())
                    if result is not None:
                        return result  # If solution found, return it
                self.undo_inferences(inferences, assignment)  # Undo inferences
                del assignment[var]  # Remove variable from assignment if no solution found
        return None  # If no solution found, return None

    def generate_puzzle(self):
        # Method to randomly generate a Tenner Grid puzzle
        for var in self.variables:
            value = random.choice(self.domain[var])
            self.grid[var[0]][var[1]] = value

    def print_grid(self):
        # Method to print the Tenner Grid puzzle
        for row in self.grid:
            print(row)

def solve_puzzle(puzzle, solver_func):
    start_time = time.time()
    puzzle.num_variable_assignments = 0
    puzzle.num_consistency_checks = 0
    assignment = solver_func({})
    end_time = time.time()
    print("Time taken to solve:", end_time - start_time, "seconds")
    print("Number of variable assignments:", puzzle.num_variable_assignments)
    print("Number of consistency checks:", puzzle.num_consistency_checks)
    print("\nFinal state:")
    puzzle.print_grid()


def main():
    num_puzzles = 10
    grid_size = 3
    solvers = {
        "Backtracking": TennerGridCSP(grid_size).backtracking_search,
        "Forward Checking": TennerGridCSP(grid_size).forward_checking,
        "Forward Checking + MRV": TennerGridCSP(grid_size).forward_checking_mrv
    }

    median_checks = {solver_name: [] for solver_name in solvers.keys()}

    for _ in range(5):  # Five runs
        algorithm_checks = {solver_name: [] for solver_name in solvers.keys()}
        for i in range(num_puzzles):
            puzzle = TennerGridCSP(grid_size)
            puzzle.generate_puzzle()
            for solver_name, solver_func in solvers.items():
                start_time = time.time()
                puzzle.num_variable_assignments = 0
                puzzle.num_consistency_checks = 0
                assignment = solver_func({})
                end_time = time.time()
                print(f"\nPuzzle {i+1} - Solving with {solver_name}:")
                print("Initial state:")
                puzzle.print_grid()
                print("Final state:")
                puzzle.print_grid() if assignment is not None else print("No solution found.")
                print("Time taken to solve:", end_time - start_time, "seconds")
                print("Number of variable assignments:", puzzle.num_variable_assignments)
                print("Number of consistency checks:", puzzle.num_consistency_checks)
                algorithm_checks[solver_name].append(puzzle.num_consistency_checks)
        # Calculate median number of consistency checks for each algorithm
        for solver_name, checks in algorithm_checks.items():
            checks.sort()
            median = checks[len(checks)//2] if len(checks) % 2 != 0 else (checks[len(checks)//2 - 1] + checks[len(checks)//2]) / 2
            median_checks[solver_name].append(median)
    
    # Calculate median of medians
    final_median_checks = {}
    for solver_name, median_list in median_checks.items():
        final_median_checks[solver_name] = sum(median_list) / len(median_list)

    # Print results
    print("\nMedian number of consistency checks over five runs:")
    for solver_name, final_median_check in final_median_checks.items():
        print(f"{solver_name}: {final_median_check}")

if __name__ == "__main__":
    main()
