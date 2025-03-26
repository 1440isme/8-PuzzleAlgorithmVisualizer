import copy

class Puzzle:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        
    def find_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j
    
    def get_possible_moves(self):
        i, j = self.find_blank_position()
        moves = []
        if i > 0: moves.append('UP')
        if i < 2: moves.append('DOWN')
        if j > 0: moves.append('LEFT')
        if j < 2: moves.append('RIGHT')
        return moves

    def get_new_state(self, move):
        i, j = self.find_blank_position()
        new_state = copy.deepcopy(self.state)
        
        if move == 'UP':
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
        elif move == 'DOWN':
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        elif move == 'LEFT':
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        elif move == 'RIGHT':
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
        
        return new_state

def is_solvable(state):
    flat_state = [state[i][j] for i in range(3) for j in range(3)]
    inversions = 0
    for i in range(len(flat_state)):
        if flat_state[i] == 0:
            continue
        for j in range(i+1, len(flat_state)):
            if flat_state[j] == 0:
                continue
            if flat_state[i] > flat_state[j]:
                inversions += 1
    return inversions % 2 == 0