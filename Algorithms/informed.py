import heapq

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

def greedy_search(initial_state, goal_state):
    queue = [(manhattan_distance(initial_state, goal_state), 0, initial_state, [])]  # (heuristic, tiebreaker, state, path)
    visited = set([str(initial_state)])
    tiebreaker = 0
    
    while queue:
        _, _, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state], len(visited)
        
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if str(new_state_tuple) not in visited:
                    tiebreaker += 1
                    h = manhattan_distance(new_state_tuple, goal_state)
                    heapq.heappush(queue, (h, tiebreaker, new_state_tuple, path + [state]))
                    visited.add(str(new_state_tuple))
    return [], len(visited)

def a_star(initial_state, goal_state):
    queue = [(manhattan_distance(initial_state, goal_state), 0, 0, initial_state, [])]  # (f_score, g_score, tiebreaker, state, path)
    visited = set([str(initial_state)])
    tiebreaker = 0
    
    while queue:
        f_score, g_score, _, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state], len(visited)
        
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if str(new_state_tuple) not in visited:
                    tiebreaker += 1
                    g_new = g_score + 1
                    h_new = manhattan_distance(new_state_tuple, goal_state)
                    f_new = g_new + h_new
                    heapq.heappush(queue, (f_new, g_new, tiebreaker, new_state_tuple, path + [state]))
                    visited.add(str(new_state_tuple))
    return [], len(visited)

def ida_star(initial_state, goal_state):
    def search(state, g_score, path, threshold, visited):
        h_score = manhattan_distance(state, goal_state)
        f_score = g_score + h_score
        
        if f_score > threshold:
            return None, f_score
        
        if state == goal_state:
            return path + [state], f_score
        
        min_f = float('inf')
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                
                if str(new_state_tuple) not in visited:
                    visited.add(str(new_state_tuple))
                    result, new_f = search(new_state_tuple, g_score + 1, path + [state], threshold, visited)
                    if result is not None:
                        return result, new_f
                    min_f = min(min_f, new_f)
                    visited.remove(str(new_state_tuple))
        
        return None, min_f

    threshold = manhattan_distance(initial_state, goal_state)
    visited = set([str(initial_state)])
    
    while True:
        result, new_threshold = search(initial_state, 0, [], threshold, visited)
        if result is not None:
            return result, len(visited)
        if new_threshold == float('inf'):
            return [], len(visited)
        threshold = new_threshold

