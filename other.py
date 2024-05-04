import random

class SimpleBacktracking:
    ROWS = 4
    COLUMNS = 10
    consistency = 0
    assignments = 0
    total_cons = 0
    total_assign = 0
    divide = 0

    @staticmethod
    def generate_grid():
        grid = [[-1 for _ in range(SimpleBacktracking.COLUMNS)] for _ in range(SimpleBacktracking.ROWS)]
        for i in range(SimpleBacktracking.ROWS):
            for j in range(SimpleBacktracking.COLUMNS):
                if random.random() < 0.5:
                    grid[i][j] = random.randint(0, 9)
        return grid

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
        # Check if num is already in the same row
        for x in range(SimpleBacktracking.COLUMNS):
            SimpleBacktracking.consistency += 1
            if grid[row][x] == num:
                return False

        # Check if num is already in the same column
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

        # Other checks for diagonals and sum constraints

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

            if 1 <= x <= 5:
                grid = SimpleBacktracking.generate_grid()
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
