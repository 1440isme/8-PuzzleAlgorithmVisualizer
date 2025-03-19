import tkinter as tk
from tkinter import ttk, messagebox
import copy
from Algorithms.uninformed import bfs, dfs, ucs, ids
from Algorithms.informed import greedy_search
from Models.puzzle import parse_state, is_solvable

class PuzzleVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle Algorithm Visualizer")
        self.geometry("1000x600")
        
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
        
        tk.Button(algorithm_frame, text="BFS", width=10, 
                  command=lambda: self.set_algorithm("BFS")).pack(side=tk.LEFT, padx=5)
        tk.Button(algorithm_frame, text="DFS", width=10,
                  command=lambda: self.set_algorithm("DFS")).pack(side=tk.LEFT, padx=5)
        tk.Button(algorithm_frame, text="UCS", width=10,
                  command=lambda: self.set_algorithm("UCS")).pack(side=tk.LEFT, padx=5)
        tk.Button(algorithm_frame, text="IDS", width=10,
                  command=lambda: self.set_algorithm("IDS")).pack(side=tk.LEFT, padx=5)
        tk.Button(algorithm_frame, text="Greedy", width=10,
                  command=lambda: self.set_algorithm("Greedy")).pack(side=tk.LEFT, padx=5)
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        input_frame = tk.Frame(main_frame, width=200)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        tk.Label(input_frame, text="START:").pack(anchor=tk.W, pady=(20, 5))
        self.start_entry = tk.Entry(input_frame, width=20)
        self.start_entry.pack(pady=5)
        self.start_entry.insert(0, "1,2,3,4,0,5,6,7,8")
        
        tk.Label(input_frame, text="END:").pack(anchor=tk.W, pady=(20, 5))
        self.end_entry = tk.Entry(input_frame, width=20)
        self.end_entry.pack(pady=5)
        self.end_entry.insert(0, "1,2,3,4,5,6,7,8,0")
        
        tk.Button(input_frame, text="PLAY", width=15, 
                  command=self.solve_puzzle).pack(pady=20)
        
        puzzle_frame = tk.Frame(main_frame)
        puzzle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(puzzle_frame, width=300, height=300, bg="white")
        self.canvas.pack(pady=20)
        
        log_frame = tk.Frame(puzzle_frame)
        log_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(log_frame, text="Log:").pack(anchor=tk.W)
        self.log_text = tk.Text(log_frame, height=10, width=50)
        self.log_text.pack(fill=tk.X, pady=5)
        
        data_frame = tk.Frame(main_frame, width=250)
        data_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        tk.Label(data_frame, text="Data Structure:").pack(anchor=tk.W, pady=5)
        self.data_text = tk.Text(data_frame, height=25, width=30)
        self.data_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        speed_frame = tk.Frame(input_frame)
        speed_frame.pack(pady=10)
        tk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(speed_frame, from_=0.1, to=2.0, resolution=0.1, 
                                    orient=tk.HORIZONTAL, length=150)
        self.speed_scale.set(0.5)
        self.speed_scale.pack(side=tk.LEFT)
        
        control_frame = tk.Frame(input_frame)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Reset", width=8, command=self.reset_puzzle).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Step", width=8, command=self.step_solution).pack(side=tk.LEFT, padx=5)
        
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
        
        start_state = parse_state(start_str)
        goal_state = parse_state(end_str)
        
        if not start_state or not goal_state:
            messagebox.showerror("Error", "Invalid state format. Use comma-separated numbers 0-8.")
            return
        if is_solvable(start_state) != is_solvable(goal_state):
            messagebox.showerror("Error", "Không thể giải được từ trạng thái bắt đầu đến trạng thái kết thúc!")
            return
        
        self.start_state = tuple(tuple(row) for row in start_state)
        self.goal_state = tuple(tuple(row) for row in goal_state)
        self.current_state = copy.deepcopy(self.start_state)
        
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"Solving with {self.algorithm.get()}...\n")
        
        algorithm = self.algorithm.get()
        if algorithm == "BFS":
            self.solution_path = bfs(self.start_state, self.goal_state)
        elif algorithm == "DFS":
            self.solution_path = dfs(self.start_state, self.goal_state)
        elif algorithm == "UCS":
            self.solution_path = ucs(self.start_state, self.goal_state)
        elif algorithm == "IDS":
            self.solution_path = ids(self.start_state, self.goal_state)
        elif algorithm == "Greedy":
            self.solution_path = greedy_search(self.start_state, self.goal_state)
        
        if self.solution_path:
            self.log_text.insert(tk.END, f"Solution found in {len(self.solution_path)-1} moves!\n")
            self.animate_solution()
        else:
            self.log_text.insert(tk.END, "No solution found!\n")
            
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
                
                if step > 0:
                    prev_state = self.solution_path[step-1]
                    moved_number = "unknown"
                    for i in range(3):
                        for j in range(3):
                            if prev_state[i][j] != 0 and state[i][j] == 0:
                                moved_number = prev_state[i][j]
                    self.log_text.insert(tk.END, f"Step {step}: Number {moved_number} moved\n")
                else:
                    self.log_text.insert(tk.END, f"Step {step}: Initial state\n")
                self.log_text.see(tk.END)
                
                self.after(delay, lambda: animate_step(step + 1))
        
        animate_step()

    def draw_puzzle(self, state, path=None):
        self.canvas.delete("all")
        cell_size = 80
        offset = 30
        
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
                                            font=("Arial", 20, "bold"), fill="black")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="light gray", outline="black", width=2)