class Backtracking:
    ROWS = 4
    COLUMNS = 10
    consistency = 0
    assignments = 0
    total_cons = 0
    total_assign = 0
    divide = 0

    @staticmethod
    def simple_backtrack(grid, row, col):
        if row == Backtracking.ROWS - 1 and col == Backtracking.COLUMNS:
            return True
        if col == Backtracking.COLUMNS:
            row += 1
            col = 0
        if grid[row][col] != -1:
            return Backtracking.simple_backtrack(grid, row, col + 1)
        for num in range(10):
            if Backtracking.is_safe(grid, row, col, num):
                grid[row][col] = num
                Backtracking.assignments += 1
                if Backtracking.simple_backtrack(grid, row, col + 1):
                    return True
        grid[row][col] = -1
        Backtracking.assignments += 1
        return False

    @staticmethod
    def is_safe(grid, row, col, num):
        for x in range(Backtracking.COLUMNS):
            Backtracking.consistency += 1
            if grid[row][x] == num:
                return False
        try:
            Backtracking.consistency += 1
            if grid[row - 1][col] == num:
                return False
        except IndexError:
            Backtracking.consistency -= 1
        try:
            Backtracking.consistency += 1
            if grid[row + 1][col] == num:
                return False
        except IndexError:
            Backtracking.consistency -= 1
        try:
            Backtracking.consistency += 1
            if grid[row][col - 1] == num:
                return False
        except IndexError:
            Backtracking.consistency -= 1
        try:
            Backtracking.consistency += 1
            if grid[row][col + 1] == num:
                return False
        except IndexError:
            Backtracking.consistency -= 1
        try:
            Backtracking.consistency += 1
            if grid[row + 1][col + 1] == num:
                return False
        except IndexError:
            Backtracking.consistency -= 1
        try:
            Backtracking.consistency += 1
            if grid[row - 1][col - 1] == num:
                return False
        except IndexError:
            Backtracking.consistency -= 1
        try:
            Backtracking.consistency += 1
            if grid[row + 1][col - 1] == num:
                return False
        except IndexError:
            Backtracking.consistency -= 1
        try:
            Backtracking.consistency += 1
            if grid[row - 1][col + 1] == num:
                return False
        except IndexError:
            Backtracking.consistency -= 1
        sum_val = 0
        for i in range(Backtracking.ROWS - 1):
            if grid[i][col] != -1:
                sum_val += grid[i][col]
        Backtracking.consistency += 1
        sum_val += num
        if sum_val > grid[Backtracking.ROWS - 1][col]:
            return False
        if row == Backtracking.ROWS - 2 and sum_val != grid[Backtracking.ROWS - 1][col]:
            return False
        return True

    @staticmethod
    def print_grid(grid):
        print("\n---------Final State---------")
        for i in range(Backtracking.ROWS):
            print("|", end="")
            for j in range(Backtracking.COLUMNS):
                print(f"{grid[i][j]:2d}", end=" ")
            print("|")
        print("------------------------------\n")

    @staticmethod
    def print_initial_state(grid):
        print("\n--------Initial State---------")
        for i in range(Backtracking.ROWS):
            print("|", end="")
            for j in range(Backtracking.COLUMNS):
                if grid[i][j] != -1:
                    print(f"{grid[i][j]:2d}", end=" ")
                else:
                    print("  ", end=" ")
            print("|")
        print("------------------------------")

    @staticmethod
    def reset_counters():
        Backtracking.divide += 1
        Backtracking.total_cons += Backtracking.consistency
        Backtracking.total_assign += Backtracking.assignments
        Backtracking.consistency = 0
        Backtracking.assignments = 0

    @staticmethod
    def main():
        grid = None
        Backtracking.divide = 0
        flag = True
        while flag:
            print("Which grid would you like to solve 1, 2, 3, 4 or 5? Type 0 if you would like to exit: ")
            x = int(input())
            if x == 0:
                flag = False
                continue
            elif x == 1:
                grid = [[-1, 6, 2, 0, -1, -1, -1, 8, 5, 7],
                        [-1, 0, 1, 7, 8, -1, -1, -1, 9, -1],
                        [-1, 4, -1, -1, 2, -1, 3, 7, -1, 8],
                        [13, 10, 8, 7, 19, 16, 11, 19, 15, 17]]
            elif x == 2:
                grid = [[-1, -1, 5, 3, -1, -1, 6, -1, -1, -1],
                        [0, 7, -1, 4, 6, 5, -1, -1, 1, 3],
                        [-1, 2, 3, 7, -1, 4, -1, 6, 5, -1],
                        [10, 13, 17, 14, 8, 16, 14, 17, 14, 12]]
            elif x == 3:
                grid = [[4, -1, -1, -1, 2, 0, -1, 1, -1, 9],
                        [7, -1, -1, 5, -1, -1, -1, 2, -1, 6],
                        [4, -1, -1, 9, 7, -1, -1, -1, -1, 3],
                        [15, 11, 10, 20, 17, 4, 23, 3, 14, 18]]
            elif x == 4:
                grid = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                        [-1, 4, -1, -1, -1, 9, -1, -1, 2, -1],
                        [-1, 1, 9, -1, -1, -1, -1, -1, -1, -1],
                        [11, 9, 6, 14, 7, 14, 11, 19, 18, 10]]
            elif x == 5:
                grid = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                        [8, 8, 4, 16, 7, 6, 14, 5, 9, 7]]
            else:
                print("Invalid Input")
                continue

            Backtracking.print_initial_state(grid)
            Backtracking.simple_backtrack(grid, 0, 0)
            Backtracking.print_grid(grid)
            Backtracking.reset_counters()
            print("Assignments:", Backtracking.total_assign)
            print("Consistency Checks:", Backtracking.total_cons)
            print("Divide by:", Backtracking.divide)


if __name__ == "__main__":
    Backtracking.main()
