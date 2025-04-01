import tkinter as tk
from tkinter import ttk, messagebox
import copy
from Algorithms.uninformed import bfs, dfs, ucs, ids
from Algorithms.informed import greedy_search, a_star, ida_star, hill_climbing, simple_hill_climbing  # Thêm import simple_hill_climbing
from Models.puzzle import is_solvable
import time

class PuzzleVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle Algorithm Visualizer")
        self.geometry("1000x800")
        
        self.algorithm = tk.StringVar(value="BFS")
        self.start_state = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.current_state = None
        self.solution_path = None
        self.current_step = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        algorithm_frame = tk.Frame(self)
        algorithm_frame.pack(pady=10)
        
        bfs_btn = tk.Button(algorithm_frame, text="BFS", width=10, 
                            command=lambda: self.set_algorithm("BFS"))
        bfs_btn.pack(side=tk.LEFT, padx=5)
        
        dfs_btn = tk.Button(algorithm_frame, text="DFS", width=10,
                            command=lambda: self.set_algorithm("DFS"))
        dfs_btn.pack(side=tk.LEFT, padx=5)
        
        ucs_btn = tk.Button(algorithm_frame, text="UCS", width=10,
                            command=lambda: self.set_algorithm("UCS"))
        ucs_btn.pack(side=tk.LEFT, padx=5)
        
        ids_btn = tk.Button(algorithm_frame, text="IDS", width=10,
                            command=lambda: self.set_algorithm("IDS"))
        ids_btn.pack(side=tk.LEFT, padx=5)
        
        greedy_btn = tk.Button(algorithm_frame, text="Greedy", width=10,
                            command=lambda: self.set_algorithm("Greedy"))
        greedy_btn.pack(side=tk.LEFT, padx=5)
        
        astar_btn = tk.Button(algorithm_frame, text="A*", width=10,
                            command=lambda: self.set_algorithm("A*"))
        astar_btn.pack(side=tk.LEFT, padx=5)
        
        idastar_btn = tk.Button(algorithm_frame, text="IDA*", width=10,
                            command=lambda: self.set_algorithm("IDA*"))
        idastar_btn.pack(side=tk.LEFT, padx=5)
        
        hillclimbing_btn = tk.Button(algorithm_frame, text="Hill Climbing", width=12,
                                     command=lambda: self.set_algorithm("Hill Climbing"))
        hillclimbing_btn.pack(side=tk.LEFT, padx=5)
        
        simplehill_btn = tk.Button(algorithm_frame, text="Simple Hill", width=12,  # Thêm nút Simple Hill
                                   command=lambda: self.set_algorithm("Simple Hill"))
        simplehill_btn.pack(side=tk.LEFT, padx=5)
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        input_frame = tk.Frame(main_frame, width=200)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Nhóm các nút liên quan đến trạng thái
        state_frame = tk.Frame(input_frame)
        state_frame.pack(pady=5)
        
        tk.Label(state_frame, text="START:").pack(anchor=tk.W)
        self.start_entry = tk.Entry(state_frame, width=20)
        self.start_entry.pack(pady=2)
        self.start_entry.insert(0, "1,2,3,4,0,5,6,7,8")
        
        tk.Label(state_frame, text="END:").pack(anchor=tk.W, pady=(5, 0))
        self.end_entry = tk.Entry(state_frame, width=20)
        self.end_entry.pack(pady=2)
        self.end_entry.insert(0, "1,2,3,4,5,6,7,8,0")
        
        # Nhóm các nút điều khiển (2 trên 2 dưới)
        control_frame = tk.Frame(input_frame)
        control_frame.pack(pady=10)
        
        # Hàng trên: Random và Play
        top_row = tk.Frame(control_frame)
        top_row.pack()
        
        random_btn = tk.Button(top_row, text="Random", width=8, 
                            command=self.randomize_start_state)
        random_btn.pack(side=tk.LEFT, padx=5)
        
        play_btn = tk.Button(top_row, text="Play", width=8, 
                            command=self.solve_puzzle)
        play_btn.pack(side=tk.LEFT, padx=5)
        
        # Hàng dưới: Reset và Step
        bottom_row = tk.Frame(control_frame)
        bottom_row.pack()
        
        reset_btn = tk.Button(bottom_row, text="Reset", width=8, 
                            command=self.reset_puzzle)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        step_btn = tk.Button(bottom_row, text="Step", width=8, 
                            command=self.step_solution)
        step_btn.pack(side=tk.LEFT, padx=5)
        
        # Nhóm thanh trượt tốc độ
        speed_frame = tk.Frame(input_frame)
        speed_frame.pack(pady=5)
        tk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(speed_frame, from_=0.1, to=2.0, resolution=0.1, 
                                    orient=tk.HORIZONTAL, length=100)
        self.speed_scale.set(0.5)
        self.speed_scale.pack(side=tk.LEFT)
        
        # Tạo content_frame để chứa puzzle và data_frame cạnh nhau
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Phần puzzle
        puzzle_frame = tk.Frame(content_frame)
        puzzle_frame.pack(side=tk.LEFT, padx=10)
        
        self.canvas = tk.Canvas(puzzle_frame, width=450, height=450, bg="white")
        self.canvas.pack(pady=20)
        
        # Phần DataStructure (chiều rộng ngang bằng puzzle)
        data_frame = tk.Frame(content_frame, width=270, height=100)
        data_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        tk.Label(data_frame, text="Data Structure:").pack(anchor=tk.W, pady=5)
        self.data_text = tk.Text(data_frame, height=25, width=50, font=("Courier", 10))
        self.data_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tạo log_frame nằm dưới tất cả
        log_frame = tk.Frame(self)
        log_frame.pack(fill=tk.X, pady=10, padx=10)
        
        tk.Label(log_frame, text="Log:").pack(anchor=tk.W)
        self.log_text = tk.Text(log_frame, height=10, width=50)
        self.log_text.pack(fill=tk.X, pady=5)
        
        self.draw_puzzle(self.start_state)

    def reset_puzzle(self):
        self.current_state = copy.deepcopy(self.start_state)
        self.draw_puzzle(self.current_state)
        self.log_text.delete(1.0, tk.END)
        self.data_text.delete(1.0, tk.END)
        self.solution_path = None
        self.current_step = 0
        self.log_text.insert(tk.END, "Puzzle reset to initial state.\n")

    def step_solution(self):
        if not self.solution_path:
            self.log_text.insert(tk.END, "Hãy giải puzzle trước khi sử dụng Step!\n")
            return
        if self.current_step >= len(self.solution_path):
            self.log_text.insert(tk.END, "Đã đến bước cuối cùng của giải pháp!\n")
            return
        
        state = self.solution_path[self.current_step]
        self.current_state = state
        self.draw_puzzle(state)
        
        if self.current_step > 0:
            prev_state = self.solution_path[self.current_step-1]
            moved_number = "unknown"
            for i in range(3):
                for j in range(3):
                    if prev_state[i][j] != 0 and state[i][j] == 0:
                        moved_number = prev_state[i][j]
            self.log_text.insert(tk.END, f"Step {self.current_step}: Number {moved_number} moved\n")
        else:
            self.log_text.insert(tk.END, f"Step {self.current_step}: Initial state\n")
        self.log_text.see(tk.END)
        
        self.current_step += 1

    def set_algorithm(self, algo):
        self.algorithm.set(algo)
        self.log_text.insert(tk.END, f"Selected algorithm: {algo}\n")
        self.log_text.see(tk.END)
        
    def solve_puzzle(self):
        start_str = self.start_entry.get()
        end_str = self.end_entry.get()
        
        start_state = self.parse_state(start_str)
        goal_state = self.parse_state(end_str)
        
        if not start_state or not goal_state:
            return
        if is_solvable(start_state) != is_solvable(goal_state):
            messagebox.showerror("Error", "Không thể giải được từ trạng thái bắt đầu đến trạng thái kết thúc!")
            return
        
        self.start_state = tuple(tuple(row) for row in start_state)
        self.goal_state = tuple(tuple(row) for row in goal_state)
        self.current_state = copy.deepcopy(self.start_state)
        
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"Solving with {self.algorithm.get()}...\n")
        
        start_time = time.time()
        if self.algorithm.get() == "BFS":
            self.solution_path, visited_count = bfs(self.start_state, self.goal_state)
        elif self.algorithm.get() == "DFS":
            self.solution_path, visited_count = dfs(self.start_state, self.goal_state)
        elif self.algorithm.get() == "UCS":
            self.solution_path, visited_count = ucs(self.start_state, self.goal_state)
        elif self.algorithm.get() == "IDS":
            self.solution_path, visited_count = ids(self.start_state, self.goal_state)
        elif self.algorithm.get() == "Greedy":
            self.solution_path, visited_count = greedy_search(self.start_state, self.goal_state)
        elif self.algorithm.get() == "A*":
            self.solution_path, visited_count = a_star(self.start_state, self.goal_state)
        elif self.algorithm.get() == "IDA*":
            self.solution_path, visited_count = ida_star(self.start_state, self.goal_state)
        elif self.algorithm.get() == "Hill Climbing":
            self.solution_path, visited_count = hill_climbing(self.start_state, self.goal_state)
        elif self.algorithm.get() == "Simple Hill":  # Thêm trường hợp cho Simple Hill Climbing
            self.solution_path, visited_count = simple_hill_climbing(self.start_state, self.goal_state)
        
        end_time = time.time()
        runtime = end_time - start_time
        
        # Kiểm tra trạng thái cuối cùng của solution_path để in thông báo
        if self.solution_path and self.solution_path[-1] == self.goal_state:
            steps = len(self.solution_path) - 1
            self.log_text.insert(tk.END, f"Solution found!\n")
            self.log_text.insert(tk.END, f"Number of steps: {steps}\n")
            self.log_text.insert(tk.END, f"Time taken: {runtime:.4f} seconds\n")
            self.log_text.insert(tk.END, f"Number of states explored: {visited_count}\n")
        else:
            self.log_text.insert(tk.END, "No solution found!\n")
            self.log_text.insert(tk.END, f"Time taken: {runtime:.4f} seconds\n")
            self.log_text.insert(tk.END, f"Number of states explored: {visited_count}\n")
        
        # Luôn hiển thị đường đi nếu solution_path không rỗng
        if self.solution_path:
            self.animate_solution()
    
    def randomize_start_state(self):
        import random
        
        # Lấy trạng thái mục tiêu
        goal_state = [int(x.strip()) for x in self.end_entry.get().split(",")]
        goal_inversions = sum(1 for i in range(len(goal_state)) for j in range(i+1, len(goal_state))
                            if goal_state[i] != 0 and goal_state[j] != 0 and goal_state[i] > goal_state[j])
        goal_parity = goal_inversions % 2
        
        # Tạo trạng thái ngẫu nhiên khả thi
        while True:
            start_state = list(range(9))
            random.shuffle(start_state)
            inversions = sum(1 for i in range(len(start_state)) for j in range(i+1, len(start_state))
                            if start_state[i] != 0 and start_state[j] != 0 and start_state[i] > start_state[j])
            if inversions % 2 == goal_parity:
                break
        
        # Cập nhật ô nhập START
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, ",".join(map(str, start_state)))
        
        # Cập nhật trạng thái hiện tại và vẽ lại
        self.start_state = [start_state[i:i+3] for i in range(0, 9, 3)]
        self.current_state = copy.deepcopy(self.start_state)
        self.draw_puzzle(self.current_state)
        self.log_text.insert(tk.END, f"Random start state generated: {','.join(map(str, start_state))}\n")
    
    def parse_state(self, state_str):
        try:
            nums = [int(x.strip()) for x in state_str.split(",")]
            if len(nums) != 9 or set(nums) != set(range(9)):
                raise ValueError("Invalid input")
            return [nums[i:i+3] for i in range(0, 9, 3)]
        except:
            messagebox.showerror("Error", "Định dạng không hợp lệ. Vui lòng nhập 9 số từ 0-8, phân tách bằng dấu phẩy (ví dụ: 1,2,3,4,0,5,6,7,8).")
            return None
            
    def animate_solution(self):
        if not self.solution_path:
            return
        
        delay = int(1000 / self.speed_scale.get())
        self.current_step = 0
        
        def animate_step(step=0):
            if step < len(self.solution_path):
                state = self.solution_path[step]
                self.current_state = state
                self.draw_puzzle(state)
                self.after(delay, lambda: animate_step(step + 1))
            else:
                # Hiển thị toàn bộ đường đi trong DataStructure
                self.data_text.delete(1.0, tk.END)
                self.data_text.insert(tk.END, "Path Taken:\n")
                for i, state in enumerate(self.solution_path):
                    self.data_text.insert(tk.END, f"Step {i}: {str(state)}\n")
                self.log_text.insert(tk.END, "Animation completed.\n")
        
        animate_step()

    def draw_puzzle(self, state, path=None):
        self.canvas.delete("all")
        cell_size = 100  
        offset = 50  
        
        colors = ["#FFD700", "#FFC700", "#FFB700", "#FFA700", "#FF9700", 
                  "#FF8700", "#FF7700", "#FF6700"]
        
        for i in range(3):
            for j in range(3):
                x0 = j * cell_size + offset
                y0 = i * cell_size + offset
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                
                if state[i][j] != 0:
                    color = colors[state[i][j]-1]
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=2)
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text=str(state[i][j]), 
                                            font=("Arial", 24, "bold"), fill="black")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="light gray", outline="black", width=2)