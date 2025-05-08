from collections import deque
import random


def is_goal(state, goal):
    return state == goal

# Hàm lấy các trạng thái lân cận (dùng ma trận 3x3)
def get_neighbors(state):
    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]

    for di, dj in moves:
        new_i, new_j = blank_i + di, blank_j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [list(row) for row in state]
            new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
            neighbors.append(tuple(tuple(row) for row in new_state))
    return neighbors

# Hàm sensor_search mô phỏng dữ liệu cảm biến
def sensor_search(state, sensor_type="local"):
    blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
    if sensor_type == "local":
        # Trả về thông tin ô lân cận của ô trống
        sensor_data = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                sensor_data.append((new_i, new_j, state[new_i][new_j]))
        return sensor_data
    elif sensor_type == "partial":
        # Trả về thông tin 3 ô ngẫu nhiên (tăng từ 2 để cải thiện)
        indices = random.sample([(i, j) for i in range(3) for j in range(3) if (i, j) != (blank_i, blank_j)], 3)
        return [(i, j, state[i][j]) for i, j in indices]
    return []

# Belief State Search
def belief_state_search(initial_state, goal_state):
    belief_state = {tuple(tuple(row) for row in initial_state)}  # Ma trận 3x3
    visited = set()
    queue = deque([(belief_state, [initial_state])])
    sensor_type = "partial"

    while queue:
        current_belief, path = queue.popleft()
        current_belief = set(current_belief)

        for state in current_belief:
            if is_goal(list(state), goal_state):
                return path, len(visited)

        # Lấy dữ liệu cảm biến từ tất cả trạng thái trong belief state
        sensor_data_sets = [sensor_search(list(state), sensor_type) for state in current_belief]
        # Giao nhau dữ liệu cảm biến để đảm bảo nhất quán
        common_sensor_data = sensor_data_sets[0]
        for sensor_data in sensor_data_sets[1:]:
            common_sensor_data = [(i, j, v) for i, j, v in common_sensor_data if (i, j, v) in sensor_data]
        if not common_sensor_data:
            continue

        # Cập nhật belief state
        new_belief = set()
        for state in current_belief:
            state = list(state)
            consistent = True
            for i, j, value in common_sensor_data:
                if state[i][j] != value:
                    consistent = False
                    break
            if consistent:
                new_belief.add(tuple(tuple(row) for row in state))

        if not new_belief:
            continue

        for state in new_belief:
            state = list(state)
            if str(state) in visited:
                continue
            visited.add(str(state))
            neighbors = get_neighbors(state)
            for neighbor in neighbors:
                queue.append((new_belief, path + [list(neighbor)]))

    return [], len(visited)

# Physical Search
def physical_search(initial_state, goal_state):
    def is_solvable(state):
        # Flatten the state for inversion count
        if isinstance(state[0], (list, tuple)):
            flat_state = [num for row in state for num in row]
        else:
            flat_state = list(state)

        inv = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if flat_state[i] != 0 and flat_state[j] != 0 and flat_state[i] > flat_state[j]:
                    inv += 1
        return inv % 2 == 0

    # Flatten initial and goal states
    initial_state_flat = tuple(num for row in initial_state for num in row)
    goal_state_flat = tuple(num for row in goal_state for num in row)

    if not is_solvable(initial_state):
        return [], 0

    # Initialize queue with initial state and empty path
    queue = deque([(initial_state_flat, [])])
    visited = {initial_state_flat}
    expansions = 0
    moves = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    while queue:
        current_state, path = queue.popleft()
        current_state_2d = [list(current_state[i:i + 3]) for i in range(0, 9, 3)]
        expansions += 1

        if current_state == goal_state_flat:
            final_path = [initial_state]
            current = initial_state_flat
            for action in path:
                zero_index = current.index(0)
                row, col = divmod(zero_index, 3)
                dr, dc = moves[action]
                new_row, new_col = row + dr, col + dc
                new_index = new_row * 3 + new_col
                new_state = list(current)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                current = tuple(new_state)
                final_path.append([list(current[i:i + 3]) for i in range(0, 9, 3)])
            return final_path, expansions

        # Get neighbors
        zero_index = current_state.index(0)
        row, col = divmod(zero_index, 3)
        for action, (dr, dc) in moves.items():
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = list(current_state)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    queue.append((new_state_tuple, path + [action]))

    return [], expansions