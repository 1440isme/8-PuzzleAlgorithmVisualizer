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

    # Chuyển initial_state và goal_state về dạng danh sách phẳng
    initial_flat = flatten_state(initial_state)
    goal_flat = flatten_state(goal_state)

    # Kiểm tra dữ liệu đầu vào
    if set(initial_flat) != set(range(9)) or set(goal_flat) != set(range(9)):
        raise ValueError("States must contain exactly the numbers 0 to 8")

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

    # Chuyển initial_state thành danh sách để dễ xử lý
    numbers = initial_flat[:]
    # Gọi Backtracking từ ô đầu tiên (pos = 0)
    success = False
    # Thử từng số trong start state làm điểm bắt đầu (dịch vòng danh sách)
    for start_idx in range(len(numbers)):
        remaining_numbers = numbers[start_idx:] + numbers[:start_idx]
        board = [[None for _ in range(3)] for _ in range(3)]
        steps = []
        visited_count = 0
        if backtrack(0, remaining_numbers):
            success = True
            break
    
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
            for xk in [v for v in csp['variables'] if v != xi and v != xj and (xk, xi) in csp['constraints']]:
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

    # Biểu diễn bài toán dưới dạng CSP
    # Biến: Mỗi ô là một biến, định dạng là tuple (i,j)
    variables = [(i, j) for i in range(3) for j in range(3)]
    
    # Miền giá trị: Ban đầu là {0,1,...,8}, nhưng nếu ô đã có giá trị thì chỉ chứa giá trị đó
    domains = {}
    for i, j in variables:
        value = initial_state[i][j]
        if value is not None:  # Ô đã có giá trị cố định từ trạng thái ban đầu
            domains[(i, j)] = [value]
        else:
            domains[(i, j)] = list(range(9))
    
    # Ràng buộc: All-Different (mỗi ô có giá trị khác nhau)
    constraints = {}
    for var1 in variables:
        for var2 in variables:
            if var1 != var2:
                constraints[(var1, var2)] = lambda x, y: x != y
    
    # Tạo CSP
    csp = {
        'variables': variables,
        'domains': domains,
        'constraints': constraints
    }
    
    # Chạy AC-3 để thu hẹp miền giá trị
    consistent, domains, ac3_log = ac3(csp)
    if not consistent:
        return [], 0, ac3_log  # Không thể giải, trả về danh sách bước rỗng
    
    # Chuyển goal state thành dạng bảng 3x3 để kiểm tra
    goal = [[goal_flat[i * 3 + j] for j in range(3)] for i in range(3)]
    # Bảng ban đầu là bảng trống
    board = [[None for _ in range(3)] for _ in range(3)]
    # Danh sách các bước để hiển thị animation
    steps = []
    # Đếm số trạng thái đã thăm
    visited_count = 0

    def backtrack(pos):
        nonlocal visited_count
        # Tính vị trí ô hiện tại (i,j) từ chỉ số pos (0 đến 8)
        i, j = divmod(pos, 3)
        var = (i, j)
        
        # Nếu đã điền hết tất cả ô (pos = 9), kiểm tra xem có khớp goal state không
        if pos == 9:
            if all(board[i][j] == goal[i][j] for i in range(3) for j in range(3)):
                steps.append([row[:] for row in board])
                return True
            return False
        
        # Nếu ô đã có giá trị cố định từ initial_state, không cần thử giá trị mới
        if initial_state[i][j] is not None:
            board[i][j] = initial_state[i][j]
            steps.append([row[:] for row in board])
            if backtrack(pos + 1):
                return True
            board[i][j] = None
            steps.append([row[:] for row in board])
            return False
        
        # Thử các giá trị trong miền đã thu hẹp
        for value in domains[var]:
            # Kiểm tra xem giá trị này có thỏa mãn ràng buộc với các ô đã điền không
            valid = True
            for k in range(3):
                for l in range(3):
                    if (k, l) != (i, j) and board[k][l] is not None:
                        if board[k][l] == value:
                            valid = False
                            break
                if not valid:
                    break
            if not valid:
                continue
            
            # Đặt số vào ô (i,j)
            board[i][j] = value
            steps.append([row[:] for row in board])
            visited_count += 1
            
            # Đệ quy để điền ô tiếp theo
            if backtrack(pos + 1):
                return True
            
            # Nếu không thành công, quay lui: bỏ số ra khỏi ô
            board[i][j] = None
            steps.append([row[:] for row in board])
        
        return False

    # Gọi Backtracking từ ô đầu tiên (pos = 0)
    success = backtrack(0)
    
    if not success:
        ac3_log.append("Backtracking failed to find a solution after AC-3.")
        return [], visited_count, ac3_log
    
    return steps, visited_count, ac3_log