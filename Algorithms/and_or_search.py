class EightPuzzleProblem:
    def __init__(self, initial, goal):
        self.initial = tuple(tuple(row) for row in initial)
        self.goal = tuple(tuple(row) for row in goal)
    
    def goal_test(self, state):
        return state == self.goal
    
    def actions(self, state):
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        return [move for di, dj, move in moves if 0 <= blank_i + di < 3 and 0 <= blank_j + dj < 3]
    
    def result(self, state, action):
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        # Chỉ giải nén 2 giá trị: di, dj
        di, dj = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}[action]
        new_i, new_j = blank_i + di, blank_j + dj
        new_state = [list(row) for row in state]
        new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
        return tuple(tuple(row) for row in new_state)

def manhattan_distance(state, goal_state):
    distance = 0
    goal_positions = {(goal_state[i][j], (i, j)) for i in range(3) for j in range(3)}
    goal_dict = dict(goal_positions)
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                goal_i, goal_j = goal_dict[state[i][j]]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def and_or_search(initial_state, goal_state):
    problem = EightPuzzleProblem(initial_state, goal_state)
    
    def or_search(state, path, visited):
        if problem.goal_test(state):
            return [], len(visited)
        if str(state) in path:
            return None, len(visited)
        
        visited.add(str(state))
        actions = problem.actions(state)
        # Sort actions by heuristic
        move_states = [(manhattan_distance(problem.result(state, action), goal_state), action) for action in actions]
        move_states.sort(key=lambda x: x[0])
        
        for _, action in move_states:
            new_state = problem.result(state, action)
            plan, _ = and_search(new_state, path + [str(state)], visited)
            if plan is not None:
                return [action] + plan, len(visited)
        return None, len(visited)
    
    def and_search(state, path, visited):
        # In deterministic 8-puzzle, AND node has one child
        return or_search(state, path, visited)
    
    visited = set()
    plan, visited_count = or_search(tuple(tuple(row) for row in initial_state), [], visited)
    if plan:
        # Reconstruct path
        path = [initial_state]
        current = tuple(tuple(row) for row in initial_state)
        for action in plan:
            current = problem.result(current, action)
            path.append([list(row) for row in current])
        return path, visited_count
    return [], visited_count