import random

class Variable:
    def __init__(self, value=-1, domain=None):
        self.value = value
        self.domain = domain if domain is not None else list(range(10))

class State:
    def __init__(self, size):
        self.rows = size
        self.vars = [Variable() for _ in range(size * 10)]
        self.goal = [0] * 10

    def print(self):
        for i in range(self.rows):
            for j in range(10):
                print(self.vars[i * 10 + j].value, end=' ')
            print()
    
    def copy(self):
        new_state = State(self.rows)
        new_state.vars = [Variable(v.value, v.domain[:]) for v in self.vars]
        new_state.goal = self.goal[:]
        return new_state
    
    def constraintCopy(self):
        return self.copy()  # For simplicity, constraintCopy behaves the same as copy in this implementation
    
    def setVar(self, index, value):
        self.vars[index].value = value

    def isSafe(self, index, value):
        row_index = index // 10
        col_index = index % 10
        
        # Check if the value is already used in the same row or column
        for i in range(self.rows):
            if self.vars[row_index * 10 + i].value == value:
                return False
            if self.vars[i * 10 + col_index].value == value:
                return False
        
        # Check if the value satisfies the goal constraint
        if self.vars[index].value == -1 and self.goal[col_index] + value > 10:
            return False
        
        return True

def generator(size):
    gen = State(size)
    row = list(range(10))

    # Fill the 1st row with numbers 0-9 randomly shuffled
    random.shuffle(row)
    for i in range(10):
        gen.vars[i].value = row[i]

    # Fill the other rows randomly
    for i in range(10, size * 10, 10):
        while True:
            random.shuffle(row)
            valid_row = True
            for j in range(10):
                if row[j] == gen.vars[j + i - 10].value or \
                   (j > 0 and row[j] == gen.vars[j + i - 10 - 1].value) or \
                   (j < 9 and row[j] == gen.vars[j + i - 10 + 1].value):
                    valid_row = False
                    break
            if valid_row:
                break
        for j in range(10):
            gen.vars[i + j].value = row[j]

    # Calculate the goal row (sum of the previous rows)
    for i in range(10):
        for j in range(size):
            gen.goal[i] += gen.vars[(j * 10) + i].value

    # Hide some numbers
    hide = random.randint(size * 10 // 4, size * 10 // 2)
    for _ in range(hide):
        h = random.randint(0, size * 10 - 1)
        gen.vars[h].value = -1
    
    return gen

def BTMRV(index, state):
    unassignedVars = sum(1 for v in state.vars if v.value == -1)
    if unassignedVars == 0:
        return True
    
    maxCons = 0
    ind = -1
    for i in range(len(state.vars)):
        if state.vars[i].value == -1:
            countCons = sum(not state.isSafe(index, i) for _ in range(10))
            if countCons > maxCons:
                maxCons = countCons
                ind = i
    
    for i in range(10):
        extraState = state.copy()
        if state.isSafe(index, i):
            state.vars[index].value = i
            if BTMRV(ind, state):
                return True
            else:
                state = extraState
    return False

def BT(index, state):
    if index >= state.rows * 10:
        state.print()
        return True

    if state.vars[index].value >= 0:
        return BT(index + 1, state)

    for i in range(10):
        extraState = state.copy()
        if state.isSafe(index, i):
            state.vars[index].value = i
            if BT(index + 1, state):
                return True
            else:
                state = extraState
    return False

def backtrack(index, state):
    if index >= state.rows * 10:
        state.print()
        return True
    
    if state.vars[index].value >= 0:
        return backtrack(index + 1, state)
    
    for i in range(10):
        if state.vars[index].domain[i] < 0:
            continue
        extraState = state.copy()
        state.setVar(index, state.vars[index].domain[i])
        if validDomains(state):
            if backtrack(index + 1, state):
                return True
            else:
                state = extraState
    return False

def validDomains(state):
    return all(v.domSize > 0 for v in state.vars)

def shuffle(array):
    random.shuffle(array)

def main():
    size = 5
    game = generator(size)
    gameState1 = game.constraintCopy()
    gameState2 = game.constraintCopy()
    gameState3 = game.constraintCopy()
    
    print("\nGame:")
    game.print()
    
    print("\nSolve by BackTrack:")
    sol = BT(0, gameState1)
    print(sol)
    
    print("\nSolve by BackTrack + MRV:")
    sol = BTMRV(0, gameState3)
    print(sol)
    
    print("\nSolve by Forward Checking:")
    solved = backtrack(0, gameState2)
    print(solved)

if __name__ == "__main__":
    main()
