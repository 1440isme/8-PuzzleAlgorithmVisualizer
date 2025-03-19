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
    queue = [(manhattan_distance(initial_state, goal_state), 0, initial_state, [])]
    visited = set([str(initial_state)])
    tiebreaker = 0
    
    while queue:
        _, _, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state]
        
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
    return []