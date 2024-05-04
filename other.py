class SimpleBacktracking:
    ROWS = 4
    COLUMNS = 10
    consistency = 0
    assignments = 0
    total_cons = 0
    total_assign = 0
    divide = 0

    @staticmethod
    def simple_backtrack(grid, row, col):
        if row == SimpleBacktracking.ROWS - 1 and col == SimpleBacktracking.COLUMNS:
            return True

        if col == SimpleBacktracking.COLUMNS:
            row += 1
            col = 0

        if grid[row][col] != -1:
            return SimpleBacktracking.simple_backtrack(grid, row, col + 1)

        for num in range(10):
            if SimpleBacktracking.is_safe(grid, row, col, num):
                grid[row][col] = num
                SimpleBacktracking.assignments += 1

                if SimpleBacktracking.simple_backtrack(grid, row, col + 1):
                    return True

        grid[row][col] = -1
        SimpleBacktracking.assignments += 1
        return False

    @staticmethod
    def is_safe(grid, row, col, num):
        for x in range(SimpleBacktracking.COLUMNS):
            SimpleBacktracking.consistency += 1
            if grid[row][x] == num:
                return False

        try:
            SimpleBacktracking.consistency += 1
            if grid[row - 1][col] == num:
                return False
        except IndexError:
            SimpleBacktracking.consistency -= 1

        try:
            SimpleBacktracking.consistency += 1
            if grid[row + 1][col] == num:
                return False
        except IndexError:
            SimpleBacktracking.consistency -= 1

        try:
            SimpleBacktracking.consistency += 1
            if grid[row][col - 1] == num:
                return False
        except IndexError:
            SimpleBacktracking.consistency -= 1

        try:
            SimpleBacktracking.consistency += 1
            if grid[row][col + 1] == num:
                return False
        except IndexError:
            SimpleBacktracking.consistency -= 1

        try:
            SimpleBacktracking.consistency += 1
            if grid[row + 1][col + 1] == num:
                return False
        except IndexError:
            SimpleBacktracking.consistency -= 1

        try:
            SimpleBacktracking.consistency += 1
            if grid[row - 1][col - 1] == num:
                return False
        except IndexError:
            SimpleBacktracking.consistency -= 1

        try:
            SimpleBacktracking.consistency += 1
            if grid[row + 1][col - 1] == num:
                return False
        except IndexError:
            SimpleBacktracking.consistency -= 1

        try:
            if grid[row - 1][col + 1] == num:
                SimpleBacktracking.consistency += 1
                return False
        except IndexError:
            SimpleBacktracking.consistency -= 1

        sum_val = 0
        for i in range(SimpleBacktracking.ROWS - 1):
            if grid[i][col] != -1:
                sum_val += grid[i][col]

        SimpleBacktracking.consistency += 1
        sum_val += num

        if sum_val > grid[SimpleBacktracking.ROWS - 1][col]:
            return False

        if row == SimpleBacktracking.ROWS - 2 and sum_val != grid[SimpleBacktracking.ROWS - 1][col]:
            return False

        return True

    @staticmethod
    def print_grid(grid):
        print("\n ---------Final State---------")
        for i in range(SimpleBacktracking.ROWS):
            print("|", end="")
            for j in range(SimpleBacktracking.COLUMNS):
                print(f"{grid[i][j]:>2} ", end="")
            print("|")
        print(" ------------------------------\n")

    @staticmethod
    def print_initial_state(grid):
        print("\n --------Initial State---------")
        for i in range(SimpleBacktracking.ROWS):
            print("|", end="")
            for j in range(SimpleBacktracking.COLUMNS):
                if grid[i][j] != -1:
                    print(f"{grid[i][j]:>2} ", end="")
                else:
                    print("   ", end="")
            print("|")
        print(" ------------------------------")

    @staticmethod
    def reset_counters():
        SimpleBacktracking.divide += 1
        SimpleBacktracking.total_cons += SimpleBacktracking.consistency
        SimpleBacktracking.total_assign += SimpleBacktracking.assignments
        SimpleBacktracking.consistency = 0
        SimpleBacktracking.assignments = 0

    @staticmethod
    def main():
        grid = None
        SimpleBacktracking.divide = 0
        flag = True

        while flag:
            x = int(input("Which grid would you like to solve 1, 2, 3, 4, or 5? Type 0 if you would like to exit: "))
            if x == 0:
                flag = False
                break

            if x == 1:
                f = [
                    [-1, 6, 2, 0, -1, -1, -1, 8, 5, 7],
                    [-1, 0, 1, 7, 8, -1, -1, -1, 9, -1],
                    [-1, 4, -1, -1, 2, -1, 3, 7, -1, 8],
                    [13, 10, 8, 7, 19, 16, 11, 19, 15, 17]
                ]
                grid = f
                SimpleBacktracking.print_initial_state(grid)
                if SimpleBacktracking.simple_backtrack(grid, 0, 0):
                    SimpleBacktracking.print_grid(grid)
                else:
                    print("No Solution exists")
            elif x == 2:
                s = [
                    [-1, -1, 5, 3, -1, -1, 6, -1, -1, -1],
                    [0, 7, -1, 4, 6, 5, -1, -1, 1, 3],
                    [-1, 2, 3, 7, -1, 4, -1, 6, 5, -1],
                    [10, 13, 17, 14, 8, 16, 14, 17, 14, 12]
                ]
                grid = s
                SimpleBacktracking.print_initial_state(grid)
                if SimpleBacktracking.simple_backtrack(grid, 0, 0):
                    SimpleBacktracking.print_grid(grid)
                else:
                    print("No Solution exists")
            elif x == 3:
                t = [
                    [4, -1, -1, -1, 2, 0, -1, 1, -1, 9],
                    [7, -1, -1, 5, -1, -1, -1, 2, -1, 6],
                    [4, -1, -1, 9, 7, -1, -1, -1, -1, 3],
                    [15, 11, 10, 20, 17, 4, 23, 3, 14, 18]
                ]
                grid = t
                SimpleBacktracking.print_initial_state(grid)
                if SimpleBacktracking.simple_backtrack(grid, 0, 0):
                    SimpleBacktracking.print_grid(grid)
                else:
                    print("No Solution exists")
            elif x == 4:
                fo = [
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, 4, -1, -1, -1, 9, -1, -1, 2, -1],
                    [-1, 1, 9, 5, 8, 4, -1, 7, 6, 3],
                    [13, 14, 20, 13, 13, 18, 10, 14, 12, 8]
                ]
                grid = fo
                SimpleBacktracking.print_initial_state(grid)
                if SimpleBacktracking.simple_backtrack(grid, 0, 0):
                    SimpleBacktracking.print_grid(grid)
                else:
                    print("No Solution exists")
            elif x == 5:
                fi = [
                    [5, 7, -1, 0, -1, 1, -1, -1, -1, -1],
                    [1, -1, -1, 6, 7, -1, -1, 5, 4, -1],
                    [-1, -1, -1, -1, -1, -1, 1, 7, 2, -1],
                    [14, 12, 17, 15, 19, 10, 14, 18, 9, 7]
                ]
                grid = fi
                SimpleBacktracking.print_initial_state(grid)
                if SimpleBacktracking.simple_backtrack(grid, 0, 0):
                    SimpleBacktracking.print_grid(grid)
                else:
                    print("No Solution exists")

            if flag:
                print("consistency:", SimpleBacktracking.consistency)
                print("assignments:", SimpleBacktracking.assignments)
                SimpleBacktracking.reset_counters()

        print("average consistency:", (SimpleBacktracking.total_cons / SimpleBacktracking.divide))
        print("average assignments:", (SimpleBacktracking.total_assign / SimpleBacktracking.divide))


if __name__ == "__main__":
    SimpleBacktracking.main()
