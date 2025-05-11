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
    
    return [], visited_count

def no_observation_solve(initial_belief_states, goal_belief_states, max_iterations=1000, time_limit=10):
    """
    Sensorless (no observation) 8-puzzle: tìm chuỗi hành động sao cho từ bất kỳ trạng thái nào trong tập khởi tạo, agent cũng đến được goal.
    Giải bằng A* trên không gian belief state (tập hợp các trạng thái vật lý).
    """
    import time
    import heapq
    from collections import deque

    class NoObsEightPuzzleProblem:
        def __init__(self, initial_beliefs, goal_states):
            self.initial_belief = set(tuple(tuple(row) for row in s) for s in initial_beliefs)
            self.goal_states = set(tuple(tuple(row) for row in s) for s in goal_states)
            self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

        def goal_test(self, belief):
            # Đúng khi belief state chỉ chứa và đủ các trạng thái goal (không thừa, không thiếu)
            return set(belief) == self.goal_states

        def get_possible_actions(self, belief):
            # Hợp các action hợp lệ từ tất cả các trạng thái trong belief
            possible_actions = set()
            for state in belief:
                blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
                for action in self.actions:
                    di, dj = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}[action]
                    new_i, new_j = blank_i + di, blank_j + dj
                    if 0 <= new_i < 3 and 0 <= new_j < 3:
                        possible_actions.add(action)
            return list(possible_actions)

        def transition(self, belief, action):
            # Áp dụng action cho tất cả các trạng thái trong belief
            next_belief = set()
            for state in belief:
                blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
                di, dj = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}[action]
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = [list(row) for row in state]
                    new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                    next_belief.add(tuple(tuple(row) for row in new_state))
                else:
                    next_belief.add(state)  # Nếu không di chuyển được thì giữ nguyên
            return next_belief

        def heuristic(self, belief):
            # Heuristic: trung bình khoảng cách Manhattan nhỏ nhất từ mỗi trạng thái đến goal
            total = 0
            for state in belief:
                min_dist = float('inf')
                for goal in self.goal_states:
                    dist = manhattan_distance(state, goal)
                    min_dist = min(min_dist, dist)
                total += min_dist
            return total / len(belief) if belief else float('inf')

    problem = NoObsEightPuzzleProblem(initial_belief_states, goal_belief_states)
    start_time = time.time()

    def a_star_search(initial_belief):
        queue = []  # (f_score, counter, belief, path)
        counter = 0
        visited = set()
        h_score = problem.heuristic(initial_belief)
        heapq.heappush(queue, (h_score, counter, initial_belief, []))
        counter += 1

        while queue and time.time() - start_time < time_limit and counter < max_iterations:
            f_score, _, belief, path = heapq.heappop(queue)
            belief_tuple = tuple(sorted(belief))
            if belief_tuple in visited:
                continue
            visited.add(belief_tuple)

            if problem.goal_test(belief):
                return path, len(visited)

            for action in problem.get_possible_actions(belief):
                next_belief = problem.transition(belief, action)
                next_tuple = tuple(sorted(next_belief))
                if next_tuple not in visited:
                    new_path = path + [action]
                    g_score = len(new_path)
                    h_score = problem.heuristic(next_belief)
                    heapq.heappush(queue, (g_score + h_score, counter, next_belief, new_path))
                    counter += 1
        return None, len(visited)

    initial_belief = set(tuple(tuple(row) for row in s) for s in initial_belief_states)
    if problem.goal_test(initial_belief):
        return [[list(row) for row in s] for s in initial_belief], 0

    plan, visited_count = a_star_search(initial_belief)
    path = []
    if plan:
        # Tái tạo đường đi các belief state
        current_belief = initial_belief
        path.append([[list(row) for row in s] for s in current_belief])
        for action in plan:
            current_belief = problem.transition(current_belief, action)
            path.append([[list(row) for row in s] for s in current_belief])
        return path, len(plan)
    return [], 0
