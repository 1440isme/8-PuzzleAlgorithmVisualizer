import time
import heapq
import random
import time
from collections import defaultdict
import numpy as np

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

# class POMDPEightPuzzleProblem:
#     def __init__(self, initial_belief_states, goal_belief_states):
#         self.initial_belief_states = [tuple(tuple(row) for row in state) for state in initial_belief_states]
#         self.goal_belief_states = [tuple(tuple(row) for row in state) for state in goal_belief_states]
#         self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
#         self.gamma = 0.9  # Hệ số chiết khấu
        
#     def goal_test(self, belief_state):
#         # Kiểm tra xem có bất kỳ trạng thái nào trong belief state trùng với goal state không
#         return any(state in self.goal_belief_states for state in belief_state)
    
#     def get_possible_states(self, belief_state):
#         return belief_state
    
#     def get_possible_actions(self, belief_state):
#         all_actions = set()
#         for state in belief_state:
#             blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
#             moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
#             for di, dj, move in moves:
#                 if 0 <= blank_i + di < 3 and 0 <= blank_j + dj < 3:
#                     all_actions.add(move)
#         return list(all_actions)
    
#     def transition(self, state, action):
#         blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
#         di, dj = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}[action]
#         new_i, new_j = blank_i + di, blank_j + dj
#         if 0 <= new_i < 3 and 0 <= new_j < 3:
#             new_state = [list(row) for row in state]
#             new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
#             return tuple(tuple(row) for row in new_state)
#         return state
    
#     def reward(self, state):
#         if state in self.goal_belief_states:
#             return 100
#         return -1
    
#     def observation(self, state):
#         # Trong bài toán 8-puzzle, chúng ta có thể quan sát đầy đủ trạng thái
#         return state

# def pomdp_solve(initial_belief_states, goal_belief_states, max_iterations=30, time_limit=5):
#     problem = POMDPEightPuzzleProblem(initial_belief_states, goal_belief_states)
#     start_time = time.time()
    
#     def heuristic(belief_state):
#         # Tính heuristic cho belief state bằng cách lấy trung bình khoảng cách Manhattan
#         total_distance = 0
#         for state in belief_state:
#             min_distance = float('inf')
#             for goal_state in goal_belief_states:
#                 distance = manhattan_distance(state, goal_state)
#                 min_distance = min(min_distance, distance)
#             total_distance += min_distance
#         return total_distance / len(belief_state)
    
#     def bfs_search(belief_state):
#         queue = [(belief_state, [])]  # (state, path)
#         visited = set()
        
#         while queue and time.time() - start_time < time_limit:
#             current_states, path = queue.pop(0)
#             state_key = str(current_states)
            
#             if state_key in visited:
#                 continue
#             visited.add(state_key)
            
#             # Kiểm tra mục tiêu
#             for state in current_states:
#                 for goal_state in goal_belief_states:
#                     if state == goal_state:
#                         return path, len(visited)
            
#             # Thử tất cả các hành động có thể
#             actions = problem.get_possible_actions(current_states)
#             for action in actions:
#                 next_states = set()
#                 for state in current_states:
#                     next_state = problem.transition(state, action)
#                     next_states.add(next_state)
#                 queue.append((tuple(next_states), path + [action]))
        
#         return None, len(visited)
    
#     def value_iteration(belief_state, depth=0, visited=None, path=None):
#         if visited is None:
#             visited = set()
#         if path is None:
#             path = []
            
#         # Kiểm tra thời gian
#         if time.time() - start_time > time_limit:
#             return None, []
            
#         if depth >= max_iterations:
#             return None, []
        
#         # Kiểm tra trạng thái đã thăm
#         state_key = str(belief_state)
#         if state_key in visited:
#             return None, []
#         visited.add(state_key)
        
#         # Kiểm tra trực tiếp xem có trạng thái nào đạt mục tiêu không
#         for state in belief_state:
#             for goal_state in goal_belief_states:
#                 if state == goal_state:
#                     return 100, path
        
#         best_value = float('-inf')
#         best_action = None
#         best_path = []
        
#         # Sắp xếp các hành động theo heuristic để tìm kiếm hiệu quả hơn
#         actions = problem.get_possible_actions(belief_state)
#         action_values = []
#         for action in actions:
#             next_states = set()
#             for state in belief_state:
#                 next_state = problem.transition(state, action)
#                 next_states.add(next_state)
#             h_value = heuristic(tuple(next_states))
#             action_values.append((h_value, action))
        
#         # Sắp xếp theo heuristic tăng dần
#         action_values.sort()
        
#         for _, action in action_values:
#             # Tính giá trị kỳ vọng cho action này
#             expected_value = 0
#             next_states = set()
            
#             for state in belief_state:
#                 next_state = problem.transition(state, action)
#                 next_states.add(next_state)
#                 expected_value += problem.reward(next_state)
            
#             # Đệ quy cho trạng thái tiếp theo
#             next_value, next_path = value_iteration(tuple(next_states), depth + 1, visited, path + [action])
            
#             # Nếu không tìm thấy đường đi, bỏ qua action này
#             if next_value is None:
#                 continue
                
#             expected_value += problem.gamma * next_value
            
#             if expected_value > best_value:
#                 best_value = expected_value
#                 best_action = action
#                 best_path = [action] + next_path
        
#         if best_action is None:
#             return None, []
            
#         return best_value, best_path
    
#     # Bắt đầu với trạng thái niềm tin ban đầu
#     initial_belief = tuple(problem.initial_belief_states)
    
#     # Kiểm tra trực tiếp xem có trạng thái nào đạt mục tiêu không
#     for state in initial_belief:
#         for goal_state in goal_belief_states:
#             if state == goal_state:
#                 return [[list(row) for row in state] for state in initial_belief], 0
    
#     # Thử tìm kiếm theo chiều rộng trước
#     bfs_result, visited_count = bfs_search(initial_belief)
#     if bfs_result is not None:
#         # Tái tạo đường đi từ kết quả BFS
#         path = []
#         current = initial_belief
        
#         # Thêm trạng thái ban đầu
#         path.append([list(row) for row in state] for state in current)
        
#         # Thêm các trạng thái trung gian
#         for action in bfs_result:
#             next_states = set()
#             for state in current:
#                 next_state = problem.transition(state, action)
#                 next_states.add(next_state)
#             current = tuple(next_states)
#             path.append([list(row) for row in state] for state in current)
            
#         return path, len(bfs_result)
    
#     # Nếu BFS không tìm thấy, thử value iteration
#     result = value_iteration(initial_belief)
    
#     if result[0] is None:
#         return [], 0
        
#     _, plan = result
    
#     if plan:
#         # Tái tạo đường đi
#         path = []
#         current = initial_belief
        
#         # Thêm trạng thái ban đầu
#         path.append([list(row) for row in state] for state in current)
        
#         # Thêm các trạng thái trung gian
#         for action in plan:
#             next_states = set()
#             for state in current:
#                 next_state = problem.transition(state, action)
#                 next_states.add(next_state)
#             current = tuple(next_states)
#             path.append([list(row) for row in state] for state in current)
            
#         return path, len(plan)
#     return [], 0


class POMDPEightPuzzleProblem:
    def __init__(self, initial_belief_states, goal_belief_states):
        self.initial_belief_states = [tuple(tuple(row) for row in state) for state in initial_belief_states]
        self.goal_belief_states = [tuple(tuple(row) for row in state) for state in goal_belief_states]
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.gamma = 0.9  # Hệ số chiết khấu
        self.observation_noise = 0.2  # Nhiễu quan sát
        self.all_states = self.initial_belief_states + self.goal_belief_states  # Danh sách trạng thái hợp lệ

    def goal_test(self, belief):
        # Kiểm tra xem trạng thái có xác suất cao nhất có trong mục tiêu không
        max_state = max(belief, key=belief.get)
        return max_state in self.goal_belief_states

    def get_possible_states(self, belief):
        return list(belief.keys())

    def get_possible_actions(self, belief):
        all_actions = set()
        for state in belief:
            blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
            moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
            for di, dj, move in moves:
                if 0 <= blank_i + di < 3 and 0 <= blank_j + dj < 3:
                    all_actions.add(move)
        return list(all_actions)

    def transition(self, state, action):
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        di, dj = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}[action]
        new_i, new_j = blank_i + di, blank_j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [list(row) for row in state]
            new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
            return tuple(tuple(row) for row in new_state)
        return state

    def reward(self, state):
        return 100 if state in self.goal_belief_states else -1

    def observation(self, state):
        # Quan sát có nhiễu
        if random.random() < self.observation_noise:
            return random.choice(self.all_states)
        return state

    def update_belief(self, belief, action, observation):
        # Cập nhật niềm tin bằng công thức Bayes
        new_belief = defaultdict(float)
        for state in belief:
            next_state = self.transition(state, action)
            prob = belief[state] * (
                (1 - self.observation_noise) if next_state == observation 
                else self.observation_noise / (len(self.all_states) - 1)
            )
            new_belief[next_state] += prob
        total = sum(new_belief.values())
        if total > 0:
            for state in new_belief:
                new_belief[state] /= total
        return dict(new_belief)

    def heuristic(self, belief):
        # Heuristic dựa trên xác suất
        total_distance = 0
        for state, prob in belief.items():
            min_distance = float('inf')
            for goal_state in self.goal_belief_states:
                distance = manhattan_distance(state, goal_state)
                min_distance = min(min_distance, distance)
            total_distance += prob * min_distance
        return total_distance

def pomdp_solve(initial_belief_states, goal_belief_states, max_iterations=100, time_limit=10):
    problem = POMDPEightPuzzleProblem(initial_belief_states, goal_belief_states)
    start_time = time.time()

    def a_star_search(initial_belief):
        queue = []  # Priority queue: (f_score, counter, belief, path)
        counter = 0  # Unique counter for tiebreaking
        visited = set()

        # Initialize queue with initial belief
        h_score = problem.heuristic(initial_belief)
        heapq.heappush(queue, (h_score, counter, initial_belief, []))
        counter += 1

        while queue and time.time() - start_time < time_limit and counter < max_iterations:
            f_score, _, belief, path = heapq.heappop(queue)
            belief_tuple = tuple(sorted(belief.items()))
            if belief_tuple in visited:
                continue
            visited.add(belief_tuple)

            if problem.goal_test(belief):
                return path, len(visited)

            for action in problem.get_possible_actions(belief):
                # Lấy trạng thái có xác suất cao nhất để tạo quan sát
                sample_state = max(belief, key=belief.get)
                next_state = problem.transition(sample_state, action)
                observation = problem.observation(next_state)
                new_belief = problem.update_belief(belief, action, observation)
                if tuple(sorted(new_belief.items())) not in visited:
                    new_path = path + [action]
                    g_score = len(new_path)
                    h_score = problem.heuristic(new_belief)
                    heapq.heappush(queue, (g_score + h_score, counter, new_belief, new_path))
                    counter += 1
        return None, len(visited)

    # Chạy A* với niềm tin ban đầu
    current = tuple(problem.initial_belief_states)
    initial_belief = {state: 1.0 / len(current) for state in current}  # Phân phối đều
    if problem.goal_test(initial_belief):
        return [[list(row) for row in state] for state in current], 0

    path = []
    plan, visited_count = a_star_search(initial_belief)
    
    if plan:
        # Tái tạo đường đi
        path.append([[list(row) for row in state] for state in current])
        current_belief = initial_belief
        for action in plan:
            sample_state = max(current_belief, key=current_belief.get)
            next_state = problem.transition(sample_state, action)
            observation = problem.observation(next_state)
            current_belief = problem.update_belief(current_belief, action, observation)
            path.append([[list(row) for row in next_state]])
        return path, len(plan)
    
    return [], 0