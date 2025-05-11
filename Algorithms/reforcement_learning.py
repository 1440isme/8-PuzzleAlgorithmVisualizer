import random
import numpy as np
from collections import defaultdict

def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # Bỏ qua ô trống
                value = state[i][j]
                # Tìm vị trí của value trong goal_state
                for gi in range(3):
                    for gj in range(3):
                        if goal_state[gi][gj] == value:
                            distance += abs(i - gi) + abs(j - gj)
                            break
    return distance

def q_learning(initial_state, goal_state, episodes=5000, alpha=0.1, gamma=0.95, epsilon_start=1.0, epsilon_end=0.01, max_steps=50):
    def get_valid_actions(state):
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = []
        if blank_i > 0: moves.append("UP")
        if blank_i < 2: moves.append("DOWN")
        if blank_j > 0: moves.append("LEFT")
        if blank_j < 2: moves.append("RIGHT")
        return moves

    def take_action(state, action):
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
        dr, dc = moves[action]
        new_i, new_j = blank_i + dr, blank_j + dc
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [list(row) for row in state]
            new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
            return tuple(tuple(row) for row in new_state)
        return state

    # Sử dụng defaultdict để tối ưu việc truy cập Q-table
    Q = defaultdict(lambda: defaultdict(float))
    visited = set()
    best_path = None
    best_path_length = float('inf')

    # Epsilon decay
    epsilon = epsilon_start
    epsilon_decay = (epsilon_start - epsilon_end) / episodes

    # Cache cho khoảng cách Manhattan
    distance_cache = {}

    for ep in range(episodes):
        state = initial_state
        visited.add(str(state))
        path = [state]
        total_reward = 0

        for step in range(max_steps):
            actions = get_valid_actions(state)
            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                q_vals = [Q[str(state)][a] for a in actions]
                action = actions[q_vals.index(max(q_vals))]

            next_state = take_action(state, action)
            visited.add(str(next_state))
            path.append(next_state)

            # Sử dụng cache cho khoảng cách Manhattan
            if str(state) not in distance_cache:
                distance_cache[str(state)] = manhattan_distance(state, goal_state)
            if str(next_state) not in distance_cache:
                distance_cache[str(next_state)] = manhattan_distance(next_state, goal_state)

            current_distance = distance_cache[str(state)]
            next_distance = distance_cache[str(next_state)]
            
            reward = 100 if next_state == goal_state else (current_distance - next_distance) * 10

            # Tối ưu việc tính max_q_next
            next_actions = get_valid_actions(next_state)
            max_q_next = max([Q[str(next_state)][a] for a in next_actions], default=0)

            # Cập nhật Q-value
            Q[str(state)][action] += alpha * (reward + gamma * max_q_next - Q[str(state)][action])

            total_reward += reward

            if next_state == goal_state:
                if len(path) < best_path_length:
                    best_path = path.copy()
                    best_path_length = len(path)
                break

            state = next_state

        # Giảm epsilon theo thời gian
        epsilon = max(epsilon_end, epsilon - epsilon_decay)

        # Kiểm tra sớm nếu đã tìm thấy đường đi tốt
        if best_path is not None and len(best_path) <= 31:  # Độ dài tối ưu cho 8-puzzle
            break

    # Nếu không tìm thấy đường đi, thử tìm đường đi tốt nhất từ Q-table
    if best_path is None:
        path = [initial_state]
        current = initial_state
        for _ in range(50):  # Giảm số bước tối đa
            if current == goal_state:
                break
            valid_actions = get_valid_actions(current)
            q_vals = [Q[str(current)][a] for a in valid_actions]
            best_action = valid_actions[q_vals.index(max(q_vals))]
            current = take_action(current, best_action)
            path.append(current)
        best_path = path

    return best_path, len(visited)
