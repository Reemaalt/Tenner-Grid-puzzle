import random
import time
from copy import deepcopy

class TennerGridCSP:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[random.randint(0, 9) for _ in range(grid_size)] for _ in range(10)]  
        self.variables = [(i, j) for i in range(10) for j in range(grid_size)]  
        self.domain = {var: list(range(10)) for var in self.variables}  
        self.constraints = self.generate_constraints()  
        self.num_variable_assignments = 0  
        self.num_consistency_checks = 0  

    def generate_constraints(self):
        constraints = {}
        for i in range(10):
            for j in range(self.grid_size - 1):
                for k in range(j + 1, self.grid_size):
                    var1 = (i, j)
                    var2 = (i, k)
                    if (var1, var2) not in constraints:
                        constraints[(var1, var2)] = []
                    for val1 in range(10):
                        for val2 in range(10):
                            if val1 != val2:
                                constraints[(var1, var2)].append((val1, val2))
        return constraints
    
    def is_consistent(self, var, value, assignment):
        for other_var in assignment:
            if other_var != var and (other_var, var) in self.constraints:
                if (assignment[other_var], value) not in self.constraints[(other_var, var)]:
                    self.num_consistency_checks += 1  
                    return False
        return True

    def select_unassigned_variable(self, assignment):
        unassigned = [(var, len(self.domain[var])) for var in self.variables if var not in assignment]
        return min(unassigned, key=lambda x: x[1])[0]

    def backtracking_search(self):
        return self.backtrack({}, self.domain)
    
    def backtrack(self, assignment, remaining):
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
        return self.forward_check({}, deepcopy(self.domain))

    def forward_check(self, assignment, remaining):
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
        return self.forward_check_mrv({}, deepcopy(self.domain))

    def forward_check_mrv(self, assignment, remaining):
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

    def calculate_remaining_values(self, var, value, assignment):
        count = 0
        for neighbor in self.variables:
            if neighbor != var and (neighbor, var) in self.constraints:
                for neighbor_value in self.domain[neighbor]:
                    if (value, neighbor_value) in self.constraints[(neighbor, var)] and neighbor not in assignment:
                        count += 1
        return count
    
    def display_grid(self):
        for row in self.grid:
            print(row)

def generate_random_puzzle(grid_size):
    puzzle = TennerGridCSP(grid_size)
    grid = [[-1 for _ in range(grid_size)] for _ in range(3)]
    for i in range(3):
        for j in range(grid_size):
            if random.random() < 0.5:
                grid[i][j] = random.randint(0, 9)
    puzzle.grid = grid
    return puzzle


def main():
    grid_size = 10  # Number of columns
    print(f"Solving 3x{grid_size} Tenner Grid Puzzle")
    print("-" * 40)

    algorithms = {
        "Simple Backtracking": TennerGridCSP.backtracking_search,
        "Forward Checking": TennerGridCSP.forward_checking,
        "Forward Checking with MRV": TennerGridCSP.forward_checking_mrv
    }

    for alg_name, algorithm in algorithms.items():
        print(f"Using {alg_name}:")
        print("-" * 40)

        consistency_checks = []
        variable_assignments = []
        start_time = time.time()

        for _ in range(5):
            puzzle = generate_random_puzzle(grid_size)
            if algorithm.__name__ == "backtracking_search":
                solution = algorithm(puzzle)
            else:
                solution = algorithm(puzzle)

            consistency_checks.append(puzzle.num_consistency_checks)
            variable_assignments.append(puzzle.num_variable_assignments)
            
            print("Initial State:")
            puzzle.display_grid()
            print("Solution:")
            puzzle.display_grid()
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
