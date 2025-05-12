import random
# Hàm backtracking_with_steps (giữ nguyên từ trước)
def backtracking_with_steps(initial_state, goal_state):
    # Hàm chuyển đổi từ dạng 3x3 (tuple/danh sách) sang danh sách phẳng
    def flatten_state(state):
        if isinstance(state, (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state):
            return [state[i][j] for i in range(3) for j in range(3)]
        elif isinstance(state, (list, tuple)) and len(state) == 9:
            return list(state)
        else:
            raise ValueError("State must be a 3x3 grid (list/tuple of lists/tuples) or a flat list/tuple with 9 elements")

    # Hàm kiểm tra tính liên tục của các số
    def is_continuous_sequence(board, pos):
        if pos == 0:  # Ô đầu tiên có thể điền bất kỳ số nào
            return True
        # Tìm số lớn nhất đã điền trước đó
        max_num = -1
        for i in range(pos):
            row, col = divmod(i, 3)
            if board[row][col] is not None:
                max_num = max(max_num, board[row][col])
        
        # Nếu đã điền đến số 8, số tiếp theo phải là 0
        if max_num == 8:
            return board[pos // 3][pos % 3] == 0
        # Ngược lại, số tiếp theo phải là max_num + 1
        return board[pos // 3][pos % 3] == max_num + 1

    # Chuyển goal_state về dạng danh sách phẳng
    goal_flat = flatten_state(goal_state)

    # Kiểm tra dữ liệu đầu vào
    if set(goal_flat) != set(range(9)):
        raise ValueError("Goal state must contain exactly the numbers 0 to 8")

    # Chuyển goal state thành dạng bảng 3x3 để dễ kiểm tra
    goal = [[goal_flat[i * 3 + j] for j in range(3)] for i in range(3)]
    # Bảng ban đầu là bảng trống
    board = [[None for _ in range(3)] for _ in range(3)]
    # Danh sách các bước để hiển thị animation
    steps = []
    # Đếm số trạng thái đã thăm
    visited_count = 0

    def backtrack(pos, remaining_numbers):
        nonlocal visited_count
        # Tính vị trí ô hiện tại (i,j) từ chỉ số pos (0 đến 8)
        i, j = divmod(pos, 3)
        
        # Nếu đã điền hết tất cả ô (pos = 9), kiểm tra xem có khớp goal state không
        if pos == 9:
            # Kiểm tra xem bảng có khớp với goal state không
            if all(board[i][j] == goal[i][j] for i in range(3) for j in range(3)):
                steps.append([row[:] for row in board])
                return True
            return False
        
        # Thử các số còn lại trong remaining_numbers
        for idx, num in enumerate(remaining_numbers):
            # Đặt số vào ô (i,j)
            board[i][j] = num
            # Kiểm tra tính liên tục
            if not is_continuous_sequence(board, pos):
                board[i][j] = None
                continue
            # Lưu trạng thái hiện tại để hiển thị animation
            steps.append([row[:] for row in board])
            visited_count += 1
            
            # Loại số này khỏi danh sách còn lại
            next_numbers = remaining_numbers[:idx] + remaining_numbers[idx+1:]
            # Đệ quy để điền ô tiếp theo
            if backtrack(pos + 1, next_numbers):
                return True
            
            # Nếu không thành công, quay lui: bỏ số ra khỏi ô
            board[i][j] = None
            # Lưu trạng thái sau khi bỏ số (để hiển thị animation)
            steps.append([row[:] for row in board])
        
        return False

    # Danh sách các số cần điền (0-8)
    numbers = list(range(9))
    random.shuffle(numbers)  # Xáo trộn ngẫu nhiên các số
    # Gọi Backtracking từ ô đầu tiên (pos = 0)
    success = backtrack(0, numbers)
    
    if not success:
        return [], visited_count
    
    return steps, visited_count

# Hàm AC-3: Đảm bảo tính nhất quán cung (arc consistency)
def ac3(csp):
    """
    Thuật toán AC-3 để đảm bảo tính nhất quán cung.
    Args:
        csp: Một dict chứa các thành phần của CSP:
            - variables: List các biến (ô trong bảng 3x3).
            - domains: Dict ánh xạ biến đến miền giá trị của nó.
            - constraints: Dict ánh xạ cặp biến (var1, var2) đến hàm kiểm tra ràng buộc.
    Returns:
        - (True, domains, ac3_log): Nếu đạt nhất quán cung, trả về True, miền giá trị đã thu hẹp, và log của AC-3.
        - (False, None, ac3_log): Nếu không thể đạt nhất quán cung (một miền rỗng), trả về False, None, và log.
    """
    # Hàng đợi chứa tất cả các cung (arcs)
    queue = [(var1, var2) for var1 in csp['variables'] for var2 in csp['variables'] if var1 != var2 and (var1, var2) in csp['constraints']]
    ac3_log = []  # Log các giá trị bị xóa để hiển thị trong visualizer
    
    while queue:
        (xi, xj) = queue.pop(0)  # Lấy cung đầu tiên từ hàng đợi
        if revise(csp, xi, xj, ac3_log):
            # Nếu miền của xi bị sửa và trở thành rỗng, trả về False
            if not csp['domains'][xi]:
                ac3_log.append(f"Domain of {xi} became empty, CSP is unsolvable.")
                return False, None, ac3_log
            # Thêm các cung (xk, xi) vào hàng đợi, với xk là hàng xóm của xi (trừ xj)
            for xk in [v for v in csp['variables'] if v != xi and v != xj and (v, xi) in csp['constraints']]:
                queue.append((xk, xi))
    
    return True, csp['domains'], ac3_log

def revise(csp, xi, xj, ac3_log):
    """
    Hàm REVISE trong AC-3: Sửa miền giá trị của xi dựa trên ràng buộc với xj.
    Args:
        csp: Bài toán CSP.
        xi, xj: Hai biến cần kiểm tra.
        ac3_log: List để ghi lại log các giá trị bị xóa.
    Returns:
        True nếu miền của xi bị sửa, False nếu không.
    """
    revised = False
    # Tạo bản sao của miền xi để tránh lỗi khi xóa phần tử trong lúc duyệt
    di = csp['domains'][xi].copy()
    for x in di:
        # Nếu không tồn tại y trong Dj thỏa mãn ràng buộc giữa xi và xj
        if not any(csp['constraints'][(xi, xj)](x, y) for y in csp['domains'][xj]):
            csp['domains'][xi].remove(x)
            ac3_log.append(f"Removed value {x} from domain of {xi} due to constraint with {xj}")
            revised = True
    return revised

# Hàm Backtracking tích hợp với AC-3
def backtracking_with_ac3(initial_state, goal_state):
    """
    Hàm Backtracking sử dụng AC-3 để giải bài toán 8-Puzzle.
    Args:
        initial_state: Trạng thái ban đầu (danh sách 3x3).
        goal_state: Trạng thái mục tiêu (danh sách 3x3).
    Returns:
        (steps, visited_count, ac3_log): Các bước giải (danh sách các trạng thái), số trạng thái đã thăm, và log của AC-3.
    """
    def flatten_state(state):
        if isinstance(state, (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state):
            return [state[i][j] for i in range(3) for j in range(3)]
        elif isinstance(state, (list, tuple)) and len(state) == 9:
            return list(state)
        else:
            raise ValueError("State must be a 3x3 grid (list/tuple of lists/tuples) or a flat list/tuple with 9 elements")

    # Hàm kiểm tra tính liên tục của các số
    def is_continuous_sequence(board, pos):
        if pos == 0:  # Ô đầu tiên có thể điền bất kỳ số nào
            return True
        # Tìm số lớn nhất đã điền trước đó
        max_num = -1
        for i in range(pos):
            row, col = divmod(i, 3)
            if board[row][col] is not None:
                max_num = max(max_num, board[row][col])
        
        # Nếu đã điền đến số 8, số tiếp theo phải là 0
        if max_num == 8:
            return board[pos // 3][pos % 3] == 0
        # Ngược lại, số tiếp theo phải là max_num + 1
        return board[pos // 3][pos % 3] == max_num + 1

    # Chuyển goal_state về dạng danh sách phẳng
    goal_flat = flatten_state(goal_state)

    # Kiểm tra dữ liệu đầu vào
    if set(goal_flat) != set(range(9)):
        raise ValueError("Goal state must contain exactly the numbers 0 to 8")

    # Biểu diễn bài toán dưới dạng CSP
    variables = [(i, j) for i in range(3) for j in range(3)]
    
    # Miền giá trị: Ban đầu tất cả ô đều có thể nhận giá trị từ 0 đến 8
    domains = {(i, j): list(range(9)) for i, j in variables}
    
    # Xáo trộn ngẫu nhiên miền giá trị của mỗi biến
    for var in variables:
        random.shuffle(domains[var])
    
    # Ràng buộc
    constraints = {}
    
    # 1. Ràng buộc All-Different
    for var1 in variables:
        for var2 in variables:
            if var1 != var2:
                constraints[(var1, var2)] = lambda x, y: x != y
    
    # 2. Ràng buộc về vị trí của số 0 (ô trống) trong goal state
    for i in range(3):
        for j in range(3):
            if goal_state[i][j] == 0:
                var = (i, j)
                for other_var in variables:
                    if other_var != var:
                        constraints[(var, other_var)] = lambda x, y, v=0: x == v
                        constraints[(other_var, var)] = lambda y, x, v=0: x == v
    
    # Tạo CSP
    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': constraints
    }
    
    # Chạy AC-3 để thu hẹp miền giá trị
    consistent, domains, ac3_log = ac3(csp)
    if not consistent:
        return [], 0, ac3_log

    # Chuyển goal state thành dạng bảng 3x3 để kiểm tra
    goal = [[goal_flat[i * 3 + j] for j in range(3)] for i in range(3)]
    board = [[None for _ in range(3)] for _ in range(3)]
    steps = []
    visited_count = 0

    def is_valid_assignment(pos, value):
        i, j = divmod(pos, 3)
        # Kiểm tra xem giá trị đã xuất hiện ở các ô trước đó chưa
        for k in range(pos):
            ki, kj = divmod(k, 3)
            if board[ki][kj] == value:
                return False
        return True

    def backtrack(pos):
        nonlocal visited_count
        i, j = divmod(pos, 3)
        
        if pos == 9:
            if all(board[i][j] == goal[i][j] for i in range(3) for j in range(3)):
                steps.append([row[:] for row in board])
                return True
            return False
        
        # Thử các giá trị trong miền đã thu hẹp
        for value in domains[(i, j)]:
            if not is_valid_assignment(pos, value):
                continue
                
            board[i][j] = value
            # Kiểm tra tính liên tục
            if not is_continuous_sequence(board, pos):
                board[i][j] = None
                continue
                
            steps.append([row[:] for row in board])
            visited_count += 1
            
            if backtrack(pos + 1):
                return True
            
            board[i][j] = None
            steps.append([row[:] for row in board])
        
        return False

    # Danh sách các số cần điền (0-8)
    numbers = list(range(9))
    random.shuffle(numbers)  # Xáo trộn ngẫu nhiên các số
    # Gọi Backtracking từ ô đầu tiên (pos = 0)
    success = backtrack(0)
    
    if not success:
        ac3_log.append("Backtracking failed to find a solution after AC-3.")
        return [], visited_count, ac3_log
    
    return steps, visited_count, ac3_log

def trial_and_error(initial_state, goal_state):
    """
    Hàm Trial and Error để giải bài toán 8-Puzzle bằng cách thử nghiệm ngẫu nhiên các nước đi.
    Args:
        initial_state: Trạng thái ban đầu (danh sách 3x3).
        goal_state: Trạng thái mục tiêu (danh sách 3x3).
    Returns:
        (steps, visited_count): Các bước giải (danh sách các trạng thái), số trạng thái đã thăm, và log rỗng.
    """
    # Chuyển trạng thái thành dạng danh sách phẳng để kiểm tra
    def flatten_state(state):
        if isinstance(state, (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state):
            return [state[i][j] for i in range(3) for j in range(3)]
        elif isinstance(state, (list, tuple)) and len(state) == 9:
            return list(state)
        else:
            raise ValueError("State must be a 3x3 grid (list/tuple of lists/tuples) or a flat list/tuple with 9 elements")

    initial_flat = flatten_state(initial_state)
    goal_flat = flatten_state(goal_state)

    # Kiểm tra dữ liệu đầu vào
    if set(initial_flat) != set(range(9)) or set(goal_flat) != set(range(9)):
        raise ValueError("States must contain exactly the numbers 0 to 8")

    # Chuyển goal state thành dạng bảng 3x3 để dễ kiểm tra
    goal = [[goal_flat[i * 3 + j] for j in range(3)] for i in range(3)]
    # Danh sách các bước để hiển thị animation
    steps = [initial_state]
    # Đếm số trạng thái đã thăm
    visited_count = 0
    # Tập các trạng thái đã thăm
    visited = {tuple(tuple(row) for row in initial_state)}

    # Hàm lấy các trạng thái lân cận
    def get_neighbors(state):
        neighbors = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        for di, dj in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                neighbors.append([row[:] for row in new_state])
        return neighbors

    # Hàm tính khoảng cách Manhattan (dùng để ưu tiên nước đi tốt hơn một chút)
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

    # Danh sách để lưu các trạng thái cần thử
    queue = [initial_state]
    max_attempts = 10000  # Tăng giới hạn để thử nhiều hơn
    attempt = 0

    while queue and attempt < max_attempts:
        current_state = queue.pop(0)
        visited_count += 1

        if all(current_state[i][j] == goal[i][j] for i in range(3) for j in range(3)):
            steps.append(current_state)
            return steps, visited_count

        neighbors = get_neighbors(current_state)
        # Lọc các trạng thái lân cận chưa thăm
        unvisited_neighbors = [n for n in neighbors if tuple(tuple(row) for row in n) not in visited]
        if unvisited_neighbors:
            # Sắp xếp các trạng thái lân cận theo khoảng cách Manhattan (ưu tiên trạng thái tốt hơn)
            scored_neighbors = [(manhattan_distance(n, goal), n) for n in unvisited_neighbors]
            scored_neighbors.sort(key=lambda x: x[0])
            # Chọn ngẫu nhiên một trong số các trạng thái tốt nhất (để giữ tính ngẫu nhiên)
            best_score = scored_neighbors[0][0]
            best_neighbors = [n for score, n in scored_neighbors if score == best_score]
            next_state = random.choice(best_neighbors)
            queue.append(next_state)
            steps.append(next_state)
            visited.add(tuple(tuple(row) for row in next_state))
        
        attempt += 1

    return [], visited_count