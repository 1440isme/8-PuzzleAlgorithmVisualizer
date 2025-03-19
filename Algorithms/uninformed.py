from collections import deque
import heapq

def bfs(initial_state, goal_state):
    queue = deque([(initial_state, [])])
    visited = set([str(initial_state)])
    
    while queue:
        state, path = queue.popleft()
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
                    queue.append((new_state_tuple, path + [state]))
                    visited.add(str(new_state_tuple))
    return []

def dfs(initial_state, goal_state, max_depth=30):
    def dfs_recursive(state, path, visited, depth):
        if state == goal_state:
            return path + [state]
        if depth >= max_depth:
            return None
        
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    result = dfs_recursive(new_state_tuple, path + [state], visited, depth + 1)
                    if result:
                        return result
        return None
    
    visited = set([initial_state])
    return dfs_recursive(initial_state, [], visited, 0) or []

def ucs(initial_state, goal_state):
    queue = [(0, 0, initial_state, [])]  # (cost, tiebreaker, state, path)
    visited = set([str(initial_state)])
    tiebreaker = 0
    
    while queue:
        cost, _, state, path = heapq.heappop(queue)
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
                    heapq.heappush(queue, (cost + 1, tiebreaker, new_state_tuple, path + [state]))
                    visited.add(str(new_state_tuple))
    return []

def ids(initial_state, goal_state):
    def dls(state, path, depth_limit, visited):
        if state == goal_state:
            return path + [state]
        if len(path) >= depth_limit:
            return None
        
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    result = dls(new_state_tuple, path + [state], depth_limit, visited)
                    if result:
                        return result
        return None
    
    visited = set()
    depth = 0
    while True:
        visited.clear()
        visited.add(str(initial_state))
        result = dls(initial_state, [], depth, visited)
        if result:
            return result
        depth += 1