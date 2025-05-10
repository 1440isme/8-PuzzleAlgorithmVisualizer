import random
import math
import copy

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
    # Chuyển đổi initial_state thành list nếu là tuple
    current_state = [list(row) for row in initial_state] if isinstance(initial_state, tuple) else initial_state
    path = [current_state]
    visited = set([str(current_state)])
    
    while True:
        # So sánh trạng thái hiện tại với goal_state
        if all(current_state[i][j] == goal_state[i][j] for i in range(3) for j in range(3)):
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
                if str(new_state) not in visited:
                    h = manhattan_distance(new_state, goal_state)
                    # Thêm vào neighbors ngay cả khi heuristic không tốt hơn
                    neighbors.append((h, new_state))
                    visited.add(str(new_state))
        
        # Nếu không có trạng thái lân cận nào, dừng lại
        if not neighbors:
            return path, len(visited)
        
        # Chọn trạng thái lân cận có heuristic nhỏ nhất
        neighbors.sort(key=lambda x: x[0])
        best_h, best_state = neighbors[0]
        
        # So sánh với trạng thái hiện tại
        current_h = manhattan_distance(current_state, goal_state)
        
        # Nếu đã thăm quá nhiều trạng thái mà không tìm thấy lời giải, dừng lại
        if len(visited) > 1000:
            return path, len(visited)
            
        # Chuyển sang trạng thái tốt nhất trong các lân cận
        current_state = best_state
        path.append(current_state)

def simple_hill_climbing(initial_state, goal_state):
    # Chuyển đổi initial_state thành list nếu là tuple
    current_state = [list(row) for row in initial_state] if isinstance(initial_state, tuple) else initial_state
    path = [current_state]
    visited = set([str(current_state)])
    
    while True:
        # So sánh trạng thái hiện tại với goal_state
        if all(current_state[i][j] == goal_state[i][j] for i in range(3) for j in range(3)):
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
                if str(new_state) not in visited:
                    h = manhattan_distance(new_state, goal_state)
                    visited.add(str(new_state))
                    # Nếu tìm thấy trạng thái lân cận đầu tiên tốt hơn, chọn ngay
                    if h <= current_h:  # Thay đổi từ < thành <=
                        current_state = new_state
                        path.append(current_state)
                        found_better = True
                        break
        
        # Nếu không tìm thấy trạng thái lân cận nào tốt hơn, dừng lại
        if not found_better or len(visited) > 1000:
            return path, len(visited)

def stochastic_hill_climbing(initial_state, goal_state):
    # Chuyển đổi initial_state thành list nếu là tuple
    current_state = [list(row) for row in initial_state] if isinstance(initial_state, tuple) else initial_state
    path = [current_state]
    visited = set([str(current_state)])
    
    while True:
        # So sánh trạng thái hiện tại với goal_state
        if all(current_state[i][j] == goal_state[i][j] for i in range(3) for j in range(3)):
            return path, len(visited)
        
        # Tìm vị trí ô trống
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        # Tính heuristic của trạng thái hiện tại
        current_h = manhattan_distance(current_state, goal_state)
        
        # Tạo danh sách các trạng thái lân cận tốt hơn hoặc bằng
        better_neighbors = []
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in current_state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                if str(new_state) not in visited:
                    h = manhattan_distance(new_state, goal_state)
                    visited.add(str(new_state))
                    # Nếu trạng thái lân cận tốt hơn hoặc bằng, thêm vào danh sách
                    if h <= current_h:  # Thay đổi từ < thành <=
                        better_neighbors.append(new_state)
        
        # Nếu không có trạng thái lân cận nào tốt hơn, dừng lại
        if not better_neighbors or len(visited) > 1000:
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

def trial_and_error_search(initial_state, goal_state, max_attempts=10000):
    current_state = initial_state
    path = [current_state]
    visited = set([str(current_state)])
    
    for _ in range(max_attempts):
        if current_state == goal_state:
            return path, len(visited)
        
        # Tìm vị trí ô trống
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        # Chọn ngẫu nhiên một hướng di chuyển
        di, dj, _ = random.choice(moves)
        new_i, new_j = blank_i + di, blank_j + dj
        
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [list(row) for row in current_state]
            new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
            new_state_tuple = tuple(tuple(row) for row in new_state)
            
            if str(new_state_tuple) not in visited:
                visited.add(str(new_state_tuple))
                current_state = new_state_tuple
                path.append(current_state)
    
    return path, len(visited)

def steepest_ascent_hill_climbing(initial_state, goal_state):
    # Chuyển đổi initial_state thành list nếu là tuple
    current_state = [list(row) for row in initial_state] if isinstance(initial_state, tuple) else initial_state
    path = [current_state]
    visited = set([str(current_state)])
    
    while True:
        # So sánh trạng thái hiện tại với goal_state
        if all(current_state[i][j] == goal_state[i][j] for i in range(3) for j in range(3)):
            return path, len(visited)
        
        # Tìm vị trí ô trống
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        # Tính heuristic của trạng thái hiện tại
        current_h = manhattan_distance(current_state, goal_state)
        best_h = float('inf')
        best_state = None
        
        # Xét tất cả các trạng thái lân cận và chọn trạng thái tốt nhất
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in current_state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                if str(new_state) not in visited:
                    h = manhattan_distance(new_state, goal_state)
                    visited.add(str(new_state))
                    # Cập nhật trạng thái tốt nhất nếu tìm thấy trạng thái tốt hơn hoặc bằng
                    if h <= best_h:  # Thay đổi từ < thành <=
                        best_h = h
                        best_state = new_state
        
        # Nếu không tìm thấy trạng thái lân cận nào tốt hơn, dừng lại
        if best_h >= current_h or len(visited) > 1000:
            return path, len(visited)
        
        # Chuyển sang trạng thái tốt nhất
        current_state = best_state
        path.append(current_state)

def beam_search(initial_state, goal_state, beam_width=3):
    queue = [(manhattan_distance(initial_state, goal_state), initial_state, [initial_state])]
    visited = set([str(initial_state)])
    
    while queue:
        # Lấy beam_width trạng thái tốt nhất từ queue
        queue = sorted(queue, key=lambda x: x[0])[:beam_width]
        next_queue = []
        
        for _, state, path in queue:
            if state == goal_state:
                return path, len(visited)
            
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
                        h = manhattan_distance(new_state_tuple, goal_state)
                        next_queue.append((h, new_state_tuple, path + [new_state_tuple]))
        
        queue = next_queue
    
    return [], len(visited)

class PuzzleState:
    def __init__(self, state, goal_state):
        # Chuyển đổi state thành list nếu là tuple
        self.state = [list(row) for row in state] if isinstance(state, tuple) else state
        self.goal_state = goal_state
        self.fitness = self.calculate_fitness()
        
    def calculate_fitness(self):
        # Tính fitness dựa trên khoảng cách Manhattan
        distance = manhattan_distance(self.state, self.goal_state)
        # Chuyển đổi khoảng cách thành fitness (khoảng cách càng nhỏ, fitness càng cao)
        return 1 / (1 + distance)
    
    def get_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j
        return None

def get_valid_moves(state):
    blank_i, blank_j = state.get_blank_position()
    moves = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_i, new_j = blank_i + di, blank_j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            moves.append((new_i, new_j))
    return moves

def create_child(parent1, parent2):
    # Tạo con từ hai cha mẹ bằng cách kết hợp các bước di chuyển
    child_state = copy.deepcopy(parent1.state)
    child = PuzzleState(child_state, parent1.goal_state)
    
    # Lấy một số bước di chuyển từ parent1 và một số từ parent2
    moves1 = get_valid_moves(parent1)
    moves2 = get_valid_moves(parent2)
    
    # Chọn ngẫu nhiên một số bước di chuyển từ mỗi cha mẹ
    num_moves = min(len(moves1), len(moves2))
    if num_moves > 0:
        crossover_point = random.randint(0, num_moves)
        moves = moves1[:crossover_point] + moves2[crossover_point:]
        
        # Áp dụng các bước di chuyển
        for new_i, new_j in moves:
            blank_i, blank_j = child.get_blank_position()
            child.state[blank_i][blank_j], child.state[new_i][new_j] = child.state[new_i][new_j], child.state[blank_i][blank_j]
            child.fitness = child.calculate_fitness()
    
    return child

def mutate(state, mutation_rate=0.1):
    if random.random() < mutation_rate:
        # Thực hiện một bước di chuyển ngẫu nhiên
        moves = get_valid_moves(state)
        if moves:
            new_i, new_j = random.choice(moves)
            blank_i, blank_j = state.get_blank_position()
            state.state[blank_i][blank_j], state.state[new_i][new_j] = state.state[new_i][new_j], state.state[blank_i][blank_j]
            state.fitness = state.calculate_fitness()
    return state

def genetic_algorithm(initial_state, goal_state, population_size=50, generations=100, mutation_rate=0.1):
    # Chuyển đổi initial_state thành list nếu là tuple
    if isinstance(initial_state, tuple):
        initial_state = [list(row) for row in initial_state]
    
    # Khởi tạo quần thể
    population = []
    for _ in range(population_size):
        state = copy.deepcopy(initial_state)
        population.append(PuzzleState(state, goal_state))
    
    best_solution = None
    best_fitness = 0
    visited = set()
    
    for generation in range(generations):
        # Sắp xếp quần thể theo fitness
        population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Cập nhật giải pháp tốt nhất
        if population[0].fitness > best_fitness:
            best_fitness = population[0].fitness
            best_solution = copy.deepcopy(population[0].state)
            
            # Kiểm tra xem đã đạt đến trạng thái đích chưa
            if manhattan_distance(best_solution, goal_state) == 0:
                return [best_solution], len(visited)
        
        # Tạo quần thể mới
        new_population = []
        
        # Giữ lại một số cá thể tốt nhất (elitism)
        elite_size = population_size // 10
        new_population.extend(population[:elite_size])
        
        # Tạo các cá thể mới thông qua lai ghép và đột biến
        while len(new_population) < population_size:
            # Chọn cha mẹ thông qua tournament selection
            parent1 = random.choice(population[:population_size//2])
            parent2 = random.choice(population[:population_size//2])
            
            # Tạo con
            child = create_child(parent1, parent2)
            
            # Đột biến
            child = mutate(child, mutation_rate)
            
            # Thêm vào quần thể mới
            new_population.append(child)
            
            # Thêm vào tập đã thăm
            visited.add(str(child.state))
        
        population = new_population
    
    # Trả về giải pháp tốt nhất tìm được
    if best_solution:
        return [best_solution], len(visited)
    return [], len(visited)