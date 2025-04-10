import tkinter as tk
from tkinter import ttk, messagebox
import copy
from Algorithms.uninformed import bfs, dfs, ucs, ids
from Algorithms.informed import greedy_search, a_star, ida_star, beam_search
from Algorithms.local_search import hill_climbing, simple_hill_climbing, stochastic_hill_climbing, simulated_annealing
from Models.puzzle import is_solvable
import time

class PuzzleVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle Algorithm Visualizer")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")  # Light gray background
        
        # Center the window on the screen
        self.center_window()
        
        # Define color scheme
        self.colors = {
            "bg": "#f0f0f0",
            "frame_bg": "#ffffff",
            "button_bg": "#4a6fa5",
            "button_fg": "#ffffff",
            "hover_bg": "#5d8bc3",
            "active_button_bg": "#2d4a6d",
            "label_fg": "#333333",
            "canvas_bg": "#ffffff",
            "puzzle_colors": ["#FF9AA2", "#FFB7B2", "#FFDAC1", "#E2F0CB", 
                             "#B5EAD7", "#C7CEEA", "#B5B9FF", "#E0BBE4"]
        }
        
        self.algorithm = tk.StringVar(value="BFS")
        self.start_state = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.current_state = None
        self.solution_path = None
        self.current_step = 0
        self.after_ids = []  # For tracking animation "after" events
        
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen"""
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position coordinates
        width = 1200
        height = 800
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position of the window
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_button(self, parent, text, command, width=10):
        """Create a styled button with hover effect"""
        button = tk.Button(parent, text=text, width=width, 
                          bg=self.colors["button_bg"], fg=self.colors["button_fg"],
                          font=("Segoe UI", 9), relief=tk.FLAT,
                          activebackground=self.colors["active_button_bg"],
                          activeforeground=self.colors["button_fg"],
                          command=command)
        
        # Add hover effect
        button.bind("<Enter>", lambda e: button.config(bg=self.colors["hover_bg"]))
        button.bind("<Leave>", lambda e: button.config(bg=self.colors["button_bg"]))
        
        return button
        
    def create_widgets(self):
        # Algorithm selection section with modern tabs
        algorithm_frame = ttk.Notebook(self)
        algorithm_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create tabs for algorithm categories
        uninformed_tab = tk.Frame(algorithm_frame, bg=self.colors["frame_bg"])
        informed_tab = tk.Frame(algorithm_frame, bg=self.colors["frame_bg"])
        local_search_tab = tk.Frame(algorithm_frame, bg=self.colors["frame_bg"])  # New tab for local search
        algorithm_frame.add(uninformed_tab, text="Uninformed Search")
        algorithm_frame.add(informed_tab, text="Informed Search")
        algorithm_frame.add(local_search_tab, text="Local Search")  # Add the new tab
        
        # Uninformed search algorithms
        bfs_btn = self.create_button(uninformed_tab, "BFS", 
                            lambda: self.set_algorithm("BFS"))
        bfs_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        dfs_btn = self.create_button(uninformed_tab, "DFS",
                            lambda: self.set_algorithm("DFS"))
        dfs_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        ucs_btn = self.create_button(uninformed_tab, "UCS",
                            lambda: self.set_algorithm("UCS"))
        ucs_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        ids_btn = self.create_button(uninformed_tab, "IDS",
                            lambda: self.set_algorithm("IDS"))
        ids_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Informed search algorithms
        greedy_btn = self.create_button(informed_tab, "Greedy",
                            lambda: self.set_algorithm("Greedy"))
        greedy_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        astar_btn = self.create_button(informed_tab, "A*",
                            lambda: self.set_algorithm("A*"))
        astar_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        idastar_btn = self.create_button(informed_tab, "IDA*",
                            lambda: self.set_algorithm("IDA*"))
        idastar_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        beamsearch_btn = self.create_button(informed_tab, "Beam Search",
                                        lambda: self.set_algorithm("Beam Search"), width=12)
        beamsearch_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Local search algorithms
        hillclimbing_btn = self.create_button(local_search_tab, "Hill Climbing", 
                                    lambda: self.set_algorithm("Hill Climbing"), width=12)
        hillclimbing_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        simplehill_btn = self.create_button(local_search_tab, "Simple Hill", 
                                   lambda: self.set_algorithm("Simple Hill"), width=12)
        simplehill_btn.pack(side=tk.LEFT, padx=5, pady=10)

        stochastichill_btn = self.create_button(local_search_tab, "Stochastic Hill",
                                     lambda: self.set_algorithm("Stochastic Hill"), width=12)
        stochastichill_btn.pack(side=tk.LEFT, padx=5, pady=10)

        simualatedannealing_btn = self.create_button(local_search_tab, "Simulated Annealing",
                                        lambda: self.set_algorithm("Simulated Annealing"), width=18)
        simualatedannealing_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Main content with card-like design
        main_frame = tk.Frame(self, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input panel with rounded corners
        input_frame = tk.Frame(main_frame, width=200, bg=self.colors["frame_bg"],
                              highlightbackground="#cccccc", highlightthickness=1)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        # Title for the input panel
        tk.Label(input_frame, text="Configuration", font=("Segoe UI", 12, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.CENTER, pady=10)
        
        # Separator
        ttk.Separator(input_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=5)
        
        # Nhóm các nút liên quan đến trạng thái
        state_frame = tk.Frame(input_frame, bg=self.colors["frame_bg"])
        state_frame.pack(pady=10, padx=15, fill=tk.X)
        
        tk.Label(state_frame, text="START STATE:", font=("Segoe UI", 9),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W)
        self.start_entry = tk.Entry(state_frame, width=20, font=("Segoe UI", 9),
                                  relief=tk.SOLID, borderwidth=1)
        self.start_entry.pack(pady=2, fill=tk.X)
        self.start_entry.insert(0, "1,2,3,4,0,5,6,7,8")
        
        tk.Label(state_frame, text="GOAL STATE:", font=("Segoe UI", 9),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W, pady=(10, 0))
        self.end_entry = tk.Entry(state_frame, width=20, font=("Segoe UI", 9),
                                relief=tk.SOLID, borderwidth=1)
        self.end_entry.pack(pady=2, fill=tk.X)
        self.end_entry.insert(0, "1,2,3,4,5,6,7,8,0")
        
        # Separator
        ttk.Separator(input_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        
        # Nhóm các nút điều khiển
        control_frame = tk.Frame(input_frame, bg=self.colors["frame_bg"])
        control_frame.pack(pady=10, fill=tk.X, padx=15)
        
        tk.Label(control_frame, text="CONTROLS", font=("Segoe UI", 9, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W)
        
        # Hàng trên: Random và Play
        top_row = tk.Frame(control_frame, bg=self.colors["frame_bg"])
        top_row.pack(pady=(10, 5), fill=tk.X)
        
        random_btn = self.create_button(top_row, "Random", self.randomize_start_state, width=8)
        random_btn.pack(side=tk.LEFT, padx=5)
        
        play_btn = self.create_button(top_row, "Play", self.solve_puzzle, width=8)
        play_btn.pack(side=tk.LEFT, padx=5)
        
        # Hàng dưới: Reset, Step, và Stop
        bottom_row = tk.Frame(control_frame, bg=self.colors["frame_bg"])
        bottom_row.pack(pady=5, fill=tk.X)
        
        reset_btn = self.create_button(bottom_row, "Reset", self.reset_puzzle, width=6)
        reset_btn.pack(side=tk.LEFT, padx=2)
        
        step_btn = self.create_button(bottom_row, "Step", self.step_solution, width=6)
        step_btn.pack(side=tk.LEFT, padx=2)
        
        # Add Stop button
        self.stop_btn = self.create_button(bottom_row, "Stop", self.stop_animation, width=6)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        self.stop_btn.config(state=tk.DISABLED)
        self.stop_btn.config(bg="#e0e0e0", fg="#888888")  # Initially disabled
        
        # Speed control with modern slider
        speed_frame = tk.Frame(input_frame, bg=self.colors["frame_bg"])
        speed_frame.pack(pady=15, fill=tk.X, padx=15)
        
        tk.Label(speed_frame, text="ANIMATION SPEED", font=("Segoe UI", 9),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W)
        
        speed_slider_frame = tk.Frame(speed_frame, bg=self.colors["frame_bg"])
        speed_slider_frame.pack(fill=tk.X, pady=5)
        
        # Add icons for slow and fast
        tk.Label(speed_slider_frame, text="🐌", font=("Segoe UI", 12),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(side=tk.LEFT)
        
        self.speed_scale = ttk.Scale(speed_slider_frame, from_=0.1, to=2.0,
                                    orient=tk.HORIZONTAL)
        self.speed_scale.set(0.5)
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(speed_slider_frame, text="🚀", font=("Segoe UI", 12),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(side=tk.LEFT)
        
        # Info section at the bottom
        info_frame = tk.Frame(input_frame, bg=self.colors["frame_bg"])
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        
        # Current algorithm display
        self.algorithm_label = tk.Label(info_frame, text="Algorithm: BFS", 
                                      font=("Segoe UI", 9, "italic"),
                                      fg=self.colors["label_fg"], bg=self.colors["frame_bg"])
        self.algorithm_label.pack(anchor=tk.W)
        
        # Tạo content_frame để chứa puzzle và data_frame cạnh nhau
        content_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure content_frame with appropriate spacing
        content_frame.grid_columnconfigure(0, weight=1)  # Left spacing
        content_frame.grid_columnconfigure(1, weight=0)  # Puzzle doesn't expand horizontally
        content_frame.grid_columnconfigure(2, weight=0)  # Data frame doesn't expand horizontally
        content_frame.grid_columnconfigure(3, weight=1)  # Right spacing
        content_frame.grid_rowconfigure(0, weight=1)     # Allow vertical expansion
        
        # Empty frame for left spacing
        tk.Frame(content_frame, bg=self.colors["bg"]).grid(row=0, column=0, sticky="nsew")
        
        # Phần puzzle - placed in center column with card design
        puzzle_frame = tk.Frame(content_frame, bg=self.colors["frame_bg"], 
                              highlightbackground="#cccccc", highlightthickness=1)
        puzzle_frame.grid(row=0, column=1, sticky="ns", padx=10)
        
        # Title for puzzle area
        tk.Label(puzzle_frame, text="8-Puzzle Board", font=("Segoe UI", 12, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(pady=(10, 5))
        
        self.canvas = tk.Canvas(puzzle_frame, bg=self.colors["canvas_bg"], width=420, height=420,
                              highlightbackground="#cccccc", highlightthickness=1)
        self.canvas.pack(padx=20, pady=20)
        
        # Phần DataStructure - with card design
        data_frame = tk.Frame(content_frame, width=350, bg=self.colors["frame_bg"],
                            highlightbackground="#cccccc", highlightthickness=1)
        data_frame.grid(row=0, column=2, sticky="ns", padx=10)
        data_frame.grid_propagate(False)  # Prevent frame from shrinking to fit contents
        
        # Configure data_frame for proper layout
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(1, weight=1)
        
        tk.Label(data_frame, text="Solution Path", font=("Segoe UI", 12, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # Custom frame for text with scrollbar
        data_text_frame = tk.Frame(data_frame, bg=self.colors["frame_bg"])
        data_text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        data_text_frame.rowconfigure(0, weight=1)
        data_text_frame.columnconfigure(0, weight=1)
        
        self.data_text = tk.Text(data_text_frame, font=("Consolas", 10), width=40, wrap=tk.WORD,
                               bg="#fafafa", relief=tk.FLAT, borderwidth=0,
                               highlightbackground="#cccccc", highlightthickness=1)
        self.data_text.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar to data text
        data_scrollbar = ttk.Scrollbar(data_text_frame, orient="vertical", command=self.data_text.yview)
        data_scrollbar.grid(row=0, column=1, sticky="ns")
        self.data_text.configure(yscrollcommand=data_scrollbar.set)
        
        # Empty frame for right spacing
        tk.Frame(content_frame, bg=self.colors["bg"]).grid(row=0, column=3, sticky="nsew")
        
        # Tạo log_frame nằm dưới tất cả with card design
        log_frame = tk.Frame(self, bg=self.colors["frame_bg"],
                           highlightbackground="#cccccc", highlightthickness=1)
        log_frame.pack(fill=tk.X, pady=10, padx=10)
        
        tk.Label(log_frame, text="Execution Log", font=("Segoe UI", 10, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        log_text_frame = tk.Frame(log_frame, bg=self.colors["frame_bg"])
        log_text_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        log_text_frame.columnconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_text_frame, height=6, width=50, font=("Consolas", 9),
                              bg="#fafafa", relief=tk.FLAT,
                              highlightbackground="#cccccc", highlightthickness=1)
        self.log_text.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        # Add scrollbar to log text
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Status bar at the very bottom
        status_frame = tk.Frame(self, bg="#e0e0e0", height=20)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = tk.Label(status_frame, text="Ready", font=("Segoe UI", 8),
                                   fg="#555555", bg="#e0e0e0")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Add resize event binding
        self.bind("<Configure>", self.on_window_resize)
        
        # Initialize current_state
        self.current_state = copy.deepcopy(self.start_state)
        
        # Draw puzzle after the window is fully initialized
        self.after(100, lambda: self.draw_puzzle(self.current_state))

    def on_window_resize(self, event):
        # Only redraw if we have a current state
        if self.current_state:
            self.draw_puzzle(self.current_state)
            
    def reset_puzzle(self):
        # Cancel any running animations
        self.stop_animation()
        
        self.current_state = copy.deepcopy(self.start_state)
        self.draw_puzzle(self.current_state)
        self.log_text.delete(1.0, tk.END)
        self.data_text.delete(1.0, tk.END)
        self.solution_path = None
        self.current_step = 0
        self.log_text.insert(tk.END, "Puzzle reset to initial state.\n")

    def step_solution(self):
        if not self.solution_path:
            self.log_text.insert(tk.END, "Please solve the puzzle before using Step!\n")
            return
        if self.current_step >= len(self.solution_path):
            self.log_text.insert(tk.END, "Reached the final step of the solution!\n")
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
        self.algorithm_label.config(text=f"Algorithm: {algo}")
        self.log_text.insert(tk.END, f"Selected algorithm: {algo}\n")
        self.log_text.see(tk.END)
        self.status_label.config(text=f"Current algorithm: {algo}")
        
    def solve_puzzle(self):
        start_str = self.start_entry.get()
        end_str = self.end_entry.get()
        
        start_state = self.parse_state(start_str)
        goal_state = self.parse_state(end_str)
        
        if not start_state or not goal_state:
            return
        if is_solvable(start_state) != is_solvable(goal_state):
            messagebox.showerror("Error", "Cannot solve from the start state to the goal state!")
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
        elif self.algorithm.get() == "Simple Hill":  
            self.solution_path, visited_count = simple_hill_climbing(self.start_state, self.goal_state)
        elif self.algorithm.get() == "Stochastic Hill":
            self.solution_path, visited_count = stochastic_hill_climbing(self.start_state, self.goal_state)
        elif self.algorithm.get() == "Simulated Annealing":
            self.solution_path, visited_count = simulated_annealing(self.start_state, self.goal_state)
        elif self.algorithm.get() == "Beam Search":
            self.solution_path, visited_count = beam_search(self.start_state, self.goal_state)
        
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
            messagebox.showerror("Error", "Invalid format. Please enter 9 numbers from 0-8, separated by commas (e.g., 1,2,3,4,0,5,6,7,8).")
            return None
            
    def animate_solution(self):
        if not self.solution_path:
            return
        
        delay = int(1000 / self.speed_scale.get())
        self.current_step = 0
        self.after_ids = []  # Track animation after_ids
        self.stop_btn.config(state=tk.NORMAL)  # Enable stop button
        
        def animate_step(step=0):
            if step < len(self.solution_path):
                state = self.solution_path[step]
                self.current_state = state
                self.draw_puzzle(state)
                after_id = self.after(delay, lambda: animate_step(step + 1))
                self.after_ids.append(after_id)  # Store the after_id
            else:
                # Animation completed
                self.after_ids = []  # Clear the list of after_ids
                self.stop_btn.config(state=tk.DISABLED)  # Disable stop button
                # Use a different style for disabled button to make it more visible
                self.stop_btn.config(bg="#e0e0e0", fg="#888888")  # Light gray background with darker text
                
                # Hiển thị toàn bộ đường đi trong DataStructure
                self.data_text.delete(1.0, tk.END)
                self.data_text.insert(tk.END, "Path Taken:\n")
                for i, state in enumerate(self.solution_path):
                    self.data_text.insert(tk.END, f"Step {i}: {str(state)}\n")
                self.log_text.insert(tk.END, "Animation completed.\n")
        
        animate_step()

    def stop_animation(self):
        """Stop the current animation"""
        # Cancel all pending "after" events
        for after_id in self.after_ids:
            self.after_cancel(after_id)
        self.after_ids = []
        
        # Update UI
        self.stop_btn.config(state=tk.DISABLED)
        self.stop_btn.config(bg="#e0e0e0", fg="#888888")
        self.log_text.insert(tk.END, "Animation stopped.\n")
        self.log_text.see(tk.END)

    def draw_puzzle(self, state, path=None):
        self.canvas.delete("all")
        
        # Get canvas dimensions with reliable defaults
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width < 50 or canvas_height < 50:  # Unrealistic small values indicate the canvas isn't ready
            canvas_width = 420
            canvas_height = 420
        
        # Calculate cell size based on available space
        puzzle_size = min(canvas_width, canvas_height) - 80  # Leave margin
        cell_size = max(puzzle_size // 3, 20)  # Ensure minimum cell size
        
        # Calculate offset to center the puzzle
        x_offset = (canvas_width - (cell_size * 3)) // 2
        y_offset = (canvas_height - (cell_size * 3)) // 2
        
        # Draw board background
        board_width = cell_size * 3
        board_height = cell_size * 3
        self.canvas.create_rectangle(
            x_offset - 10, 
            y_offset - 10,
            x_offset + board_width + 10,
            y_offset + board_height + 10,
            fill="#f5f5f5", outline="#dddddd", width=2
        )
        
        # First, draw the grid with borders to ensure all cells have borders
        for i in range(4):
            # Horizontal lines
            self.canvas.create_line(
                x_offset, y_offset + i * cell_size,
                x_offset + 3 * cell_size, y_offset + i * cell_size,
                fill="#666666", width=1
            )
            # Vertical lines
            self.canvas.create_line(
                x_offset + i * cell_size, y_offset,
                x_offset + i * cell_size, y_offset + 3 * cell_size,
                fill="#666666", width=1
            )
        
        # Then draw the individual cell content
        for i in range(3):
            for j in range(3):
                x0 = j * cell_size + x_offset
                y0 = i * cell_size + y_offset
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                
                if state[i][j] != 0:
                    # Create shadow
                    self.canvas.create_rectangle(
                        x0 + 3, y0 + 3, 
                        x1 + 3, y1 + 3, 
                        fill="#bbbbbb", outline=""
                    )
                    
                    # Create tile
                    color = self.colors["puzzle_colors"][state[i][j]-1]
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, 
                        fill=color, outline="#666666", 
                        width=1
                    )
                    
                    # Add number with subtle shadow for 3D effect
                    self.canvas.create_text(
                        (x0+x1)//2 + 1, (y0+y1)//2 + 1, 
                        text=str(state[i][j]), 
                        font=("Segoe UI", int(cell_size//3), "bold"), 
                        fill="#333333"
                    )
                else:
                    # Empty space with clear border
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, 
                        fill="#eeeeee", outline="#666666", 
                        width=1
                    )
