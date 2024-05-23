import time
import random

numOfConsistencyChecks = 0
numOfVariableAssignments = 0

board = [
    [-1, -1, -1, -1 , -1, -1 , -1, -1, -1, -1],
    [-1, -1, -1, -1 , -1, -1,  -1, -1, -1 ,-1],
    [-1, -1, -1, -1 , -1, -1,  -1, -1, -1, -1],
    [-1, -1, -1, -1 , -1, -1,  -1, -1, -1, -1]
]


def initial_state(): 
    #initializes 
    global board 
    #randomzies the first row
    domain = [0,1,2,3,4,5,6,7,8,9]
    for j in range(len(board[0])):
        num = random.choice(domain)
        board[0][j] = num
        domain.remove(num)

    #randomzies the third row
    domain = [0,1,2,3,4,5,6,7,8,9]
    for j in range(len(board[2])):
        num = random.choice(domain)
        board[2][j] = num
        domain.remove(num)
    
    domain = [0,1,2,3,4,5,6,7,8,9]
    positions = [0,1,2,3,4,5,6,7,8,9]
    count = 0
    finish = False

    #randomizes the 2nd row and makes the 2nd row numbers to make it all valid
    while find_empty(board)!=None:
        position = random.choice(positions)
        if position >= 1 and position<=8:
            num = random.choice(check_surround(board, position))
        else:
            num = random.choice(domain)
        count+=1
        if valid(board, num, (1,position), False):
            count = 0
            board[1][position] = num
            domain.remove(num)
            positions.remove(position)
        #have to check this
        if count >= 1000:
            return
    
    #this is for calculating sum for 4th row
    for i in range(len(board[3])):
        board[3][i] = board[0][i] + board[1][i] + board[2][i]                                            
    count = 0
    sets = []
    
    #this makes 14 empty plots
    while count != 14:
        row = random.randint(0,2)
        col = random.randint(0,9)
        if board[row][col] != -1:
            sets.append((row, col))
            count+=1
            board[row][col] = -1
    if backtrack(board):
        for i in sets:
            row, col = i
            if board[row][col] != -1:
                count+=1
                board[row][col] = -1

        if forward_checking(board):
            for i in sets:
                row, col = i
                if board[row][col] != -1:
                    count+=1
                    board[row][col] = -1
                if forward_checking_with_mrv(board):
                    for i in sets:
                        row, col = i
                        if board[row][col] != -1:
                            count+=1
                            board[row][col] = -1           
                    return board
                else:
                    return None
            else:
                return None
        else:
            return None
    else:
        return None

    #checks connecting cells except for right and left.
def check_surround(board, pos):
    domain = [0,1,2,3,4,5,6,7,8,9]
    try:
        domain.remove(board[2][pos])
    except ValueError:
        pass
    try:
        domain.remove(board[0][pos])
    except ValueError:
        pass
    if pos != 0:
        try:
            domain.remove(board[2][pos-1])
        except ValueError:
            pass
        try:
            domain.remove(board[0][pos-1])
        except ValueError:
            pass
    if pos != 9:
        try:
            domain.remove(board[2][pos+1])
        except ValueError:
            pass
        try:
            domain.remove(board[0][pos+1])
        except ValueError:
            pass
    return domain

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[3][j] >= 10 and i != 3:
                print(f"  {board[i][j]} ", end="")
            elif board[i][j] == -1:
                print(f"{board[i][j]} ", end="")
            else:
                print(f"  {board[i][j]}", end="")
        print()


def find_empty(board):
    for i in range(len(board)-1):
        for j in range(len(board[0])):
            if board[i][j] == -1:
                return (i, j)
    return None


def valid(board, num, pos, check_sum):
    # checks if row will be valid
    global numOfConsistencyChecks
    numOfConsistencyChecks+=1
    for i in range(len(board[0])):
        tmp = board[pos[0]][i]
        if tmp == num:
            if pos[1] != i:
                return False

    if (check_sum == True):
        # checks if sum will be valid
        sum = 0
        # if the row is 2
        if pos[0] == 2:
            if board[0][pos[1]] < 0:
                num1 = 0
            else:
                num1 = board[0][pos[1]]

            if board[1][pos[1]] < 0:
                num2 = 0
            else:
                num2 = board[1][pos[1]]
            sum = num1 + num2 + num

            if sum != board[3][pos[1]]:
                return False
        # if the row is 1
        elif pos[0] == 1:
            if board[0][pos[1]] < 0:
                num1 = 0
            else:
                num1 = board[0][pos[1]]
            if board[2][pos[1]] < 0:
                num2 = 0
            else:
                num2 = board[2][pos[1]]
            sum = num1+num2 + num
            if sum > board[3][pos[1]]:
                return False
        # if the row is 0
        elif pos[0] == 0:
            if board[2][pos[1]] < 0:
                num1 = 0
            else:
                num1 = board[2][pos[1]]
            if board[1][pos[1]] < 0:
                num2 = 0
            else:
                num2 = board[1][pos[1]]
            sum = num1+num2+num
            if sum > board[3][pos[1]]:
                return False

    # checks connected cells
    try:
        if pos[0] - 1 >=0:
            num1 = board[pos[0]-1][pos[1]]
        else:
            num1 = None
    except IndexError:
        num1 = None
    try:
        num2 = board[pos[0]+1][pos[1]]
    except IndexError:
        num2 = None
    try:
        if pos[1] -1 >= 0:
            num3 = board[pos[0]][pos[1]-1]
        else:
            num3 = None
    except IndexError:
        num3 = None
    try:
        num4 = board[pos[0]][pos[1]+1]
    except IndexError:
        num4 = None
    try:
        if pos[0]-1 >= 0 and pos[1]-1 >=0:
            num5 = board[pos[0]-1][pos[1]-1]
        else:
            num5 = None
    except IndexError:
        num5 = None
    try:
        if pos[0]-1 >= 0:
            num6 = board[pos[0]-1][pos[1]+1]
        else:
            num6 = None
    except IndexError:
        num6 = None
    try:
        if pos[1] -1 >= 0:
            num7 = board[pos[0]+1][pos[1]-1]
        else:
            num7 = None
    except IndexError:
        num7 = None
    try:
        num8 = board[pos[0]+1][pos[1]+1]
    except IndexError:
        num8 = None
    # have to check for more diagonols
    if num1 == num or num2 == num or num3 == num or num4 == num or num5 == num or num6 == num or num7 == num or num8 == num:
        return False
    return True


def backtrack(board):

    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(0, 10):
        if valid(board, i, (row, col), True):
            board[row][col] = i
            global numOfVariableAssignments
            numOfVariableAssignments+=1

            if backtrack(board):
                return True

            board[row][col] = -1
    return False


def get_domain_of_all_board(board):
    domain = [
        [[], [], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], [], []]
    ]
    for i in range(len(board)-1):  # goes thru every row except sum
        for j in range(len(board[0])):  # 0-9
            for k in range(0, 10):
                if board[i][j] == -1 and valid(board, k, (i, j), False):
                    domain[i][j].append(k)
    return domain


def get_min_domain(board):
    domain = get_domain_of_all_board(board)
    min_domain = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    min_position = None
    #finds the plot with the the smallest size domain (available numbers to it) and returns it
    for i in range(len(board)-1):
        for j in range(len(board[0])):
            if domain[i][j] != [] and len(domain[i][j]) < len(min_domain):
                min_domain = domain[i][j]
                min_position = (i, j)
            #if the length of the domain and minimum domian equal, we get their degree (tie braker) 
            # the tiebreaking wins for the plot with the most ammount of connecting cells.   
            elif domain[i][j] != [] and len(domain[i][j]) == len(min_domain):
                domain_degree = get_degree((i, j))
                min_domain_degree = get_degree(min_position)
                if domain_degree >= min_domain_degree:
                    min_domain = domain[i][j]
                    min_position = (i, j)

    return min_position



def test_find_empty(board):
    for i in range(3):
        for j in range(10):
            if board[i][j] == -1:
                return False
    return True


#gets the ammount of empty plots around the given pos
def get_degree(pos):
    count = 0
    i, j = pos
    try:
        if board[i+1][j] == -1:
            count += 1
    except IndexError:
        pass
    try:
        if board[i+1][j-1] == -1 and j - 1 >= 0:
            count += 1
    except IndexError:
        pass
    try:
        if board[i+1][j+1] == -1:
            count += 1
    except IndexError:
        pass
    try:
        if board[i][j-1] == -1 and j - 1 >= 0:
            count += 1
    except IndexError:
        pass
    try:
        if board[i][j+1] == -1:
            count += 1
    except IndexError:
        pass
    try:
        if board[i-1][j+1] == -1 and i - 1 >= 0:
            count += 1
    except IndexError:
        pass
    try:
        if board[i-1][j] == -1 and i - 1 >= 0:
            count += 1
    except IndexError:
        pass
    try:
        if board[i-1][j-1] == -1 and i - 1 >= 0 and j - 1 >= 0:
            count += 1
    except IndexError:
        pass
    return count




def forward_checking(board):

    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    domain = get_domain_of_all_board(board)

    for i in domain[row][col]:
        # if i isnt in board[row] then checks validity
        if valid(board, i, (row, col), True):
            board[row][col] = i
            global numOfVariableAssignments
            numOfVariableAssignments+=1

            if forward_checking(board):  # recursive
                return True

            board[row][col] = -1

    return False


def forward_checking_with_mrv(board):

    find = get_min_domain(board)
    if not find:
        return True
    else:
        row, col = find

    domain = get_domain_of_all_board(board)

    for i in domain[row][col]:

        # if i isnt in board[row] then checks validity
        if valid(board, i, (row, col), True):
            board[row][col] = i
            global numOfVariableAssignments
            numOfVariableAssignments+=1

            if forward_checking_with_mrv(board):  # recursive
                return True

            board[row][col] = -1

    return False

import time

def main():
    board = initial_state()
    while board is None:
        board = [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]
        board = initial_state()

    num_of_runs = 5
    algorithms = {
        "1": "Backtrack",
        "2": "Forward checking",
        "3": "Forward checking with MRV"
    }
    results = {algo: {"consistency_checks": [], "variable_assignments": [], "times": []} for algo in algorithms.values()}

    for _ in range(num_of_runs):
        board = initial_state()
        if board is None:
            continue
        
        print(f"Initial State ({_ + 1}/{num_of_runs}):")
        for row in board:
            print(row)
        
        variable_assignments = 0

        for algo_num, algo_name in algorithms.items():
            print(f"Running {algo_name} ({_ + 1}/{num_of_runs})")

            board_copy = [row[:] for row in board]

            start_time = time.time()
            if algo_num == "1":
                backtrack(board_copy)
                print(f"Final CSP Tenner:")
                print_board(board_copy)
                print("\n")
            elif algo_num == "2":
                forward_checking(board_copy)
                print_board(board_copy)
                print("\n")
            elif algo_num == "3":
                forward_checking_with_mrv(board_copy)
                print_board(board_copy)
                print("\n")
            end_time = time.time()

            consistency_checks = numOfConsistencyChecks
            variable_assignments = numOfVariableAssignments
            time_taken = (end_time - start_time) * 10**9

            print(f"Consistency checks: {consistency_checks}")
            print(f"Variable assignments: {variable_assignments}")
            print(f"Time elapsed: {time_taken} nanoseconds")

            results[algo_name]["consistency_checks"].append(consistency_checks)
            results[algo_name]["variable_assignments"].append(variable_assignments)
            results[algo_name]["times"].append(time_taken)
        
        print(f"Final CSP Tenner:")
        print_board(board_copy)
        print("\n")

    # Analyze the median number of consistency checks
    print("Median Number of Consistency Checks:")
    for algo_name, data in results.items():
        median_checks = sorted(data["consistency_checks"])[len(data["consistency_checks"]) // 2]
        print(f"{algo_name}: {median_checks}")
    # Compare algorithms based on median consistency checks
    median_checks_sorted = sorted([(algo_name, sorted(data["consistency_checks"])[len(data["consistency_checks"]) // 2]) for algo_name, data in results.items()], key=lambda x: x[1])
    print(f"\nBest algorithm based on median consistency checks: {median_checks_sorted[0][0]}")

main()

