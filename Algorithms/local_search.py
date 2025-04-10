import random
import math

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

def hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]
    visited = set([str(current_state)])
    
    while True:
        if current_state == goal_state:
            return path, len(visited)
        
        # Tìm vị trí ô trống
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        # Tạo danh sách các trạng thái lân cận và tính heuristic
        neighbors = []
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in current_state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if str(new_state_tuple) not in visited:
                    h = manhattan_distance(new_state_tuple, goal_state)
                    neighbors.append((h, new_state_tuple))
                    visited.add(str(new_state_tuple))
        
        # Nếu không có trạng thái lân cận nào, dừng lại (cực đại cục bộ)
        if not neighbors:
            return path, len(visited)
        
        # Chọn trạng thái lân cận có heuristic nhỏ nhất (dốc nhất)
        neighbors.sort(key=lambda x: x[0])  # Sắp xếp theo heuristic
        best_h, best_state = neighbors[0]
        
        # So sánh với trạng thái hiện tại
        current_h = manhattan_distance(current_state, goal_state)
        if best_h >= current_h:  # Nếu không có trạng thái nào tốt hơn, dừng lại
            return path, len(visited)
        
        # Chuyển sang trạng thái tốt hơn
        current_state = best_state
        path.append(current_state)

def simple_hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]
    visited = set([str(current_state)])
    
    while True:
        if current_state == goal_state:
            return path, len(visited)
        
        # Tìm vị trí ô trống
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        # Tính heuristic của trạng thái hiện tại
        current_h = manhattan_distance(current_state, goal_state)
        found_better = False
        
        # Xét lần lượt các trạng thái lân cận
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in current_state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if str(new_state_tuple) not in visited:
                    h = manhattan_distance(new_state_tuple, goal_state)
                    visited.add(str(new_state_tuple))
                    # Nếu tìm thấy trạng thái lân cận đầu tiên tốt hơn, chọn ngay
                    if h < current_h:
                        current_state = new_state_tuple
                        path.append(current_state)
                        found_better = True
                        break
        
        # Nếu không tìm thấy trạng thái lân cận nào tốt hơn, dừng lại
        if not found_better:
            return path, len(visited)

def stochastic_hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]
    visited = set([str(current_state)])
    
    while True:
        if current_state == goal_state:
            return path, len(visited)
        
        # Tìm vị trí ô trống
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        # Tính heuristic của trạng thái hiện tại
        current_h = manhattan_distance(current_state, goal_state)
        
        # Tạo danh sách các trạng thái lân cận tốt hơn
        better_neighbors = []
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in current_state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if str(new_state_tuple) not in visited:
                    h = manhattan_distance(new_state_tuple, goal_state)
                    visited.add(str(new_state_tuple))
                    # Nếu trạng thái lân cận tốt hơn, thêm vào danh sách
                    if h < current_h:
                        better_neighbors.append(new_state_tuple)
        
        # Nếu không có trạng thái lân cận nào tốt hơn, dừng lại
        if not better_neighbors:
            return path, len(visited)
        
        # Chọn ngẫu nhiên một trạng thái từ các trạng thái lân cận tốt hơn
        current_state = random.choice(better_neighbors)
        path.append(current_state)

def simulated_annealing(initial_state, goal_state, initial_temperature=1000, cooling_rate=0.995, max_iterations=10000):
    current_state = initial_state
    path = [current_state]
    visited = set([str(current_state)])
    temperature = initial_temperature
    
    for iteration in range(max_iterations):
        if current_state == goal_state:
            return path, len(visited)
        
        # Tìm vị trí ô trống
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        # Tạo danh sách các trạng thái lân cận
        neighbors = []
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in current_state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if str(new_state_tuple) not in visited:
                    neighbors.append(new_state_tuple)
                    visited.add(str(new_state_tuple))
        
        # Nếu không có trạng thái lân cận nào, dừng lại
        if not neighbors:
            return path, len(visited)
        
        # Chọn ngẫu nhiên một trạng thái lân cận
        next_state = random.choice(neighbors)
        
        # Tính heuristic của trạng thái hiện tại và trạng thái lân cận
        current_h = manhattan_distance(current_state, goal_state)
        next_h = manhattan_distance(next_state, goal_state)
        
        # Tính độ chênh lệch heuristic (deltaE)
        delta_e = next_h - current_h
        
        # Nếu trạng thái lân cận tốt hơn (heuristic nhỏ hơn), chuyển sang trạng thái đó
        if delta_e < 0:
            current_state = next_state
            path.append(current_state)
        else:
            # Nếu trạng thái lân cận xấu hơn, chuyển sang với xác suất e^(-deltaE/T)
            probability = math.exp(-delta_e / temperature)
            if random.random() < probability:
                current_state = next_state
                path.append(current_state)
        
        # Giảm nhiệt độ
        temperature *= cooling_rate
        
        # Nếu nhiệt độ quá thấp, dừng lại
        if temperature < 0.1:
            break
    
    return path, len(visited)
