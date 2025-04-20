from collections import deque
import heapq

def bfs(initial_state, goal_state):
    queue = deque([(initial_state, [])])
    visited = set([str(initial_state)])
    
    while queue:
        state, path = queue.popleft()
        if state == goal_state:
            return path + [state], len(visited)
        
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for di, dj, move_name in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if str(new_state_tuple) not in visited:
                    queue.append((new_state_tuple, path + [state]))
                    visited.add(str(new_state_tuple))
    return [], len(visited)  # Đã đúng: trả về [] nếu không tìm thấy goal_state

def bfs_belief(initial_belief, goal_state):
    # initial_belief: dict {state_tuple: probability}
    queue = deque([(initial_belief, [])])
    visited = set([str(tuple(sorted(initial_belief.keys())))])
    
    while queue:
        belief, path = queue.popleft()
        # Kiểm tra nếu tất cả trạng thái trong belief đều là goal_state
        if all(state == tuple(tuple(row) for row in goal_state) for state in belief):
            return path + [belief], len(visited)
        
        # Các hành động: lên, xuống, trái, phải
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for di, dj, move_name in moves:
            new_belief = {}
            valid_move = True
            # Áp dụng hành động cho từng trạng thái trong belief
            for state in belief:
                state_list = [[state[i][j] for j in range(3)] for i in range(3)]
                blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state_list[i][j] == 0][0]
                new_i, new_j = blank_i + di, blank_j + dj
                # Kiểm tra hành động hợp lệ: trong lưới và không vào hàng 1
                if 0 <= new_i < 3 and 0 <= new_j < 3 and new_i >= 1:
                    new_state = [list(row) for row in state_list]
                    new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                    new_state_tuple = tuple(tuple(row) for row in new_state)
                    new_belief[new_state_tuple] = belief[state]
                else:
                    valid_move = False
                    break
            
            if valid_move and new_belief:
                belief_key = str(tuple(sorted(new_belief.keys())))
                if belief_key not in visited:
                    queue.append((new_belief, path + [belief]))
                    visited.add(belief_key)
    
    return [], len(visited)

def dfs(initial_state, goal_state, max_depth=30):
    def dfs_recursive(state, path, visited, depth):
        if state == goal_state:
            return path + [state], len(visited)
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
    
    visited = set([str(initial_state)])
    result = dfs_recursive(initial_state, [], visited, 0)
    if result:
        return result
    return [], len(visited)  # Đã đúng: trả về [] nếu không tìm thấy goal_state

def ucs(initial_state, goal_state):
    queue = [(0, 0, initial_state, [])]  # (cost, tiebreaker, state, path)
    visited = set([str(initial_state)])
    tiebreaker = 0
    
    while queue:
        cost, _, state, path = heapq.heappop(queue)
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
                    heapq.heappush(queue, (cost + 1, tiebreaker, new_state_tuple, path + [state]))
                    visited.add(str(new_state_tuple))
    return [], len(visited)  # Đã đúng: trả về [] nếu không tìm thấy goal_state

def ids(initial_state, goal_state):
    def dls(state, path, depth_limit, visited):
        if state == goal_state:
            return path + [state], len(visited)
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
                if str(new_state_tuple) not in visited:
                    visited.add(str(new_state_tuple))
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
        if depth > 50:  # Thêm giới hạn để tránh vòng lặp vô hạn
            return [], len(visited)
    return [], len(visited)  # Đã đúng: trả về [] nếu không tìm thấy goal_state