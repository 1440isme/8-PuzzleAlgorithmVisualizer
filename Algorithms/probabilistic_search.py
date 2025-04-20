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
    visited = set()
    queue = deque([(initial_state, [initial_state])])
    sensor_type = "local"

    while queue:
        state, path = queue.popleft()
        state_tuple = tuple(tuple(row) for row in state)

        if str(state_tuple) in visited:
            continue
        visited.add(str(state_tuple))

        if is_goal(state, goal_state):
            return path, len(visited)

        sensor_data = sensor_search(state, sensor_type)
        neighbors = []
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        for i, j, value in sensor_data:
            new_state = [list(row) for row in state]
            new_state[blank_i][blank_j], new_state[i][j] = new_state[i][j], new_state[blank_i][blank_j]
            neighbors.append(tuple(tuple(row) for row in new_state))

        for neighbor in neighbors:
            queue.append((list(neighbor), path + [list(neighbor)]))

    return [], len(visited)