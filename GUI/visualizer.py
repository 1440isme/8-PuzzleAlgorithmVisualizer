import tkinter as tk
from tkinter import ttk, messagebox
import copy
from Algorithms.uninformed import bfs, dfs, ucs, ids
from Algorithms.informed import greedy_search, a_star, ida_star
from Algorithms.local_search import (hill_climbing, simple_hill_climbing, 
                                   stochastic_hill_climbing, simulated_annealing,
                                   beam_search, steepest_ascent_hill_climbing, genetic_algorithm)
from Algorithms.complex import and_or_search, pomdp_solve, no_observation_solve
from Algorithms.constraint import backtracking_with_steps, backtracking_with_ac3, trial_and_error
from Algorithms.reforcement_learning import q_learning
from Models.puzzle import is_solvable
import time

class PuzzleVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle Algorithm Visualizer")
        self.geometry("1200x1200")
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
        
        # Thêm biến để lưu trạng thái hiện tại của start và goal
        self.current_start_str = "1,2,3,4,0,5,6,7,8"
        self.current_goal_str = "1,2,3,4,5,6,7,8,0"
        
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen"""
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position coordinates
        width = 1200
        height = 880
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
        local_search_tab = tk.Frame(algorithm_frame, bg=self.colors["frame_bg"])  
        complex_tab = tk.Frame(algorithm_frame, bg=self.colors["frame_bg"])  
        csp_tab = tk.Frame(algorithm_frame, bg=self.colors["frame_bg"])
        reinforcement_tab = tk.Frame(algorithm_frame, bg=self.colors["frame_bg"])
        algorithm_frame.add(uninformed_tab, text="Uninformed Search")
        algorithm_frame.add(informed_tab, text="Informed Search")
        algorithm_frame.add(local_search_tab, text="Local Search") 
        algorithm_frame.add(complex_tab, text="Complex Environment")  
        algorithm_frame.add(csp_tab, text="Constraint Satisfaction")
        algorithm_frame.add(reinforcement_tab, text="Reinforcement Learning")

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

        steepestascenthill_btn = self.create_button(local_search_tab, "Steepest Ascent Hill",
                                     lambda: self.set_algorithm("Steepest Ascent Hill"), width=18)
        steepestascenthill_btn.pack(side=tk.LEFT, padx=5, pady=10)

        simualatedannealing_btn = self.create_button(local_search_tab, "Simulated Annealing",
                                        lambda: self.set_algorithm("Simulated Annealing"), width=18)
        simualatedannealing_btn.pack(side=tk.LEFT, padx=5, pady=10)

        genetic_btn = self.create_button(local_search_tab, "Genetic Algorithm",
                                        lambda: self.set_algorithm("Genetic Algorithm"), width=18)
        genetic_btn.pack(side=tk.LEFT, padx=5, pady=10)

        beamsearch_btn = self.create_button(local_search_tab, "Beam Search",
                                        lambda: self.set_algorithm("Beam Search"), width=12)
        beamsearch_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # AND-OR search algorithm
        andor_btn = self.create_button(complex_tab, "AND-OR Search", 
                                   lambda: self.set_algorithm("AND-OR Search"), width=14)
        andor_btn.pack(side=tk.LEFT, padx=5, pady=10)

        # Thêm nút POMDP vào tab Complex Environment
        pomdp_btn = self.create_button(complex_tab, "Partially Observable", 
                                   lambda: self.set_algorithm("Partially Observable"), width=18)
        pomdp_btn.pack(side=tk.LEFT, padx=5, pady=10)

        no_observation_btn = self.create_button(complex_tab, "No Observation", 
                                   lambda: self.set_algorithm("No Observation"), width=18)
        no_observation_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Constraint Satisfaction algorithms
        backtracking_csp_btn = self.create_button(csp_tab, "Backtracking CSP", 
                               lambda: self.set_algorithm("Backtracking CSP"), width=15)
        backtracking_csp_btn.pack(side=tk.LEFT, padx=5, pady=10)

        backtracking_ac3_btn = self.create_button(csp_tab, "Backtracking - AC-3", 
                               lambda: self.set_algorithm("Backtracking - AC-3"), width=15)
        backtracking_ac3_btn.pack(side=tk.LEFT, padx=5, pady=10)

        trialanderror_btn = self.create_button(csp_tab, "Trial and Error",
                                        lambda: self.set_algorithm("Trial and Error"), width=18)
        trialanderror_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Reinforcement Learning algorithms
        q_learning_btn = self.create_button(reinforcement_tab, "Q-Learning",
                               lambda: self.set_algorithm("Q-Learning"), width=15)
        q_learning_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Main content with card-like design
        main_frame = tk.Frame(self, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tạo frame chính cho 3 khung
        top_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        top_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Input panel with rounded corners
        input_frame = tk.Frame(top_frame, width=200, bg=self.colors["frame_bg"],
                              highlightbackground="#cccccc", highlightthickness=1)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Title for the input panel
        tk.Label(input_frame, text="Configuration", font=("Segoe UI", 12, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.CENTER, pady=10)
        
        # Separator
        ttk.Separator(input_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=5)
        
        # Thay đổi phần nhập trạng thái để hỗ trợ nhiều dòng
        state_frame = tk.Frame(input_frame, bg=self.colors["frame_bg"])
        state_frame.pack(pady=10, padx=15, fill=tk.X)
        
        tk.Label(state_frame, text="START STATE:", font=("Segoe UI", 9),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W)
        
        # Thay thế Entry bằng Text cho start state
        self.start_text = tk.Text(state_frame, width=20, height=3, font=("Segoe UI", 9),
                                relief=tk.SOLID, borderwidth=1)
        self.start_text.pack(pady=2, fill=tk.X)
        self.start_text.insert("1.0", "1,2,3,4,0,5,6,7,8")
        
        tk.Label(state_frame, text="GOAL STATE:", font=("Segoe UI", 9),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W, pady=(10, 0))
        
        # Thay thế Entry bằng Text cho goal state
        self.end_text = tk.Text(state_frame, width=20, height=3, font=("Segoe UI", 9),
                              relief=tk.SOLID, borderwidth=1)
        self.end_text.pack(pady=2, fill=tk.X)
        self.end_text.insert("1.0", "1,2,3,4,5,6,7,8,0")
        
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
        
        self.speed_scale = ttk.Scale(speed_slider_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL)
        self.speed_scale.set(1.0)  # Giá trị mặc định
        
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
        
        # Phần puzzle - placed in center with card design
        puzzle_frame = tk.Frame(top_frame, bg=self.colors["frame_bg"], 
                              highlightbackground="#cccccc", highlightthickness=1)
        puzzle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Title for puzzle area
        tk.Label(puzzle_frame, text="8-Puzzle Board", font=("Segoe UI", 12, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(pady=(10, 5))
        
        self.canvas = tk.Canvas(puzzle_frame, bg=self.colors["canvas_bg"], width=420, height=420,
                              highlightbackground="#cccccc", highlightthickness=1)
        self.canvas.pack(padx=20, pady=20)
        
        # Phần DataStructure - with card design
        data_frame = tk.Frame(top_frame, width=350, bg=self.colors["frame_bg"],
                            highlightbackground="#cccccc", highlightthickness=1)
        data_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
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
        
        # Tạo frame cho phần dưới (log và comparison)
        bottom_frame = tk.Frame(self, bg=self.colors["bg"])
        bottom_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Tạo log_frame với card design
        log_frame = tk.Frame(bottom_frame, bg=self.colors["frame_bg"],
                           highlightbackground="#cccccc", highlightthickness=1)
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(log_frame, text="Execution Log", font=("Segoe UI", 10, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        log_text_frame = tk.Frame(log_frame, bg=self.colors["frame_bg"])
        log_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        log_text_frame.columnconfigure(0, weight=1)
        log_text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_text_frame, height=8, width=50, font=("Consolas", 9),
                              bg="#fafafa", relief=tk.FLAT,
                              highlightbackground="#cccccc", highlightthickness=1)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar to log text
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Tạo comparison_frame với card design
        comparison_frame = tk.Frame(bottom_frame, bg=self.colors["frame_bg"],
                                  highlightbackground="#cccccc", highlightthickness=1)
        comparison_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(comparison_frame, text="Algorithm Comparison", font=("Segoe UI", 10, "bold"),
                fg=self.colors["label_fg"], bg=self.colors["frame_bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Tạo Treeview cho bảng so sánh
        self.comparison_tree = ttk.Treeview(comparison_frame, columns=("Algorithm", "Time", "States"),
                                          show="headings", height=8)
        self.comparison_tree.heading("Algorithm", text="Algorithm Name", 
                                   command=lambda: self.sort_comparison("Algorithm"))
        self.comparison_tree.heading("Time", text="Time (s)", 
                                   command=lambda: self.sort_comparison("Time"))
        self.comparison_tree.heading("States", text="States Explored", 
                                   command=lambda: self.sort_comparison("States"))
        
        # Đặt độ rộng cột và căn giữa
        self.comparison_tree.column("Algorithm", width=150, anchor="center")
        self.comparison_tree.column("Time", width=100, anchor="center")
        self.comparison_tree.column("States", width=150, anchor="center")
        
        # Thêm thanh cuộn
        comparison_scrollbar = ttk.Scrollbar(comparison_frame, orient="vertical", 
                                           command=self.comparison_tree.yview)
        self.comparison_tree.configure(yscrollcommand=comparison_scrollbar.set)
        
        # Đóng gói Treeview và thanh cuộn
        self.comparison_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        comparison_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        
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
        self.clear_comparison()
        self.current_start_str = self.start_text.get("1.0", tk.END).strip()

    def step_solution(self):
        if not self.solution_path:
            self.log_text.insert(tk.END, "Please solve the puzzle before using Step!\n")
            return
        if self.current_step >= len(self.solution_path):
            self.log_text.insert(tk.END, "Reached the final step of the solution!\n")
            return
        
        state = self.solution_path[self.current_step]
        # Chuyển đổi trạng thái thành danh sách 3x3 nếu cần (tùy thuộc vào thuật toán)
        if isinstance(state, (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state):
            state = [list(row) for row in state]
        else:
            state = [list(state[i:i+3]) for i in range(0, 9, 3)]
        self.current_state = state
        self.draw_puzzle(state)
        
        if self.algorithm.get() in ["Backtracking CSP", "Backtracking - AC-3", "Trial and Error"]:
            # Với Backtracking, hiển thị số được đặt hoặc bỏ đi
            if self.current_step > 0:
                prev_state = self.solution_path[self.current_step-1]
                # Chuyển đổi prev_state thành danh sách 3x3 nếu cần
                if isinstance(prev_state, (list, tuple)) and len(prev_state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in prev_state):
                    prev_state = [list(row) for row in prev_state]
                else:
                    prev_state = [list(prev_state[i:i+3]) for i in range(0, 9, 3)]
                # Tìm ô thay đổi
                for i in range(3):
                    for j in range(3):
                        if prev_state[i][j] != state[i][j]:
                            if state[i][j] is not None:
                                self.log_text.insert(tk.END, f"Step {self.current_step}: Placed {state[i][j]} at position ({i},{j})\n")
                            else:
                                self.log_text.insert(tk.END, f"Step {self.current_step}: Removed {prev_state[i][j]} from position ({i},{j})\n")
                            break
        else:
            # Logic cũ cho các thuật toán khác (dựa trên số di chuyển)
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
        # Lưu thuật toán cũ trước khi thay đổi
        old_algo = self.algorithm.get()
        
        self.algorithm.set(algo)
        self.algorithm_label.config(text=f"Algorithm: {algo}")
        self.log_text.insert(tk.END, f"Selected algorithm: {algo}\n")
        self.log_text.see(tk.END)
        self.status_label.config(text=f"Current algorithm: {algo}")
        
        # Xóa nội dung ô nhập start state cho AC-3 và Backtracking
        if algo in ["Backtracking CSP", "Backtracking - AC-3"]:
            self.start_text.delete("1.0", tk.END)
            # Clear puzzle về trạng thái trống
            self.start_state = [[None, None, None], [None, None, None], [None, None, None]]
            self.current_state = copy.deepcopy(self.start_state)
            self.draw_puzzle(self.current_state)
        # Reset goal state về dạng phổ biến khi chuyển từ thuật toán mù sang thuật toán khác
        elif old_algo in ["Partially Observable", "No Observation"] and algo not in ["Partially Observable", "No Observation"]:
            self.end_text.delete("1.0", tk.END)
            self.end_text.insert("1.0", "1,2,3,4,5,6,7,8,0")
        
    def solve_puzzle(self):
        # Kiểm tra xem state có thay đổi không
        self.check_state_changed()
        
        # Bỏ qua việc kiểm tra đầu vào cho Backtracking CSP và Backtracking - AC-3
        if self.algorithm.get() not in ["Backtracking CSP", "Backtracking - AC-3"]:
            start_str = self.start_text.get("1.0", tk.END).strip()
            end_str = self.end_text.get("1.0", tk.END).strip()
            
            start_state = self.parse_state(start_str)
            goal_state = self.parse_state(end_str)
            
            if not start_state or not goal_state:
                return
                
            # Kiểm tra tính khả thi cho POMDP
            if self.algorithm.get() == "Partially Observable" or self.algorithm.get() == "No Observation":
                if not isinstance(start_state, list) or not isinstance(goal_state, list):
                    messagebox.showerror("Error", "For Partially Observable, please enter multiple states (one per line)")
                    return
                for state in start_state:
                    if not is_solvable(state):
                        messagebox.showerror("Error", "One or more start states are not solvable!")
                        return
                for state in goal_state:
                    if not is_solvable(state):
                        messagebox.showerror("Error", "One or more goal states are not solvable!")
                        return
            else:
                # Kiểm tra bình thường cho các thuật toán khác
                if is_solvable(start_state) != is_solvable(goal_state):
                    messagebox.showerror("Error", "Cannot solve from the start state to the goal state!")
                    return
            
            self.start_state = start_state
            self.goal_state = goal_state
            # Lấy trạng thái đầu tiên để hiển thị
            if isinstance(start_state, list):
                self.current_state = copy.deepcopy(start_state[0])
            else:
                self.current_state = copy.deepcopy(start_state)
        else:
            # Không cần trạng thái ban đầu cho Backtracking CSP và Backtracking - AC-3
            self.start_state = [[None, None, None], [None, None, None], [None, None, None]]
            self.current_state = copy.deepcopy(self.start_state)
            goal_str = self.end_text.get("1.0", tk.END).strip()
            self.goal_state = self.parse_state(goal_str)
            if not self.goal_state:
                return
        
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"Solving with {self.algorithm.get()}...\n")
        
        start_time = time.time()
        
        # Thêm xử lý cho POMDP
        if self.algorithm.get() == "Partially Observable":
            self.solution_path, visited_count = pomdp_solve(start_state, goal_state)
        elif self.algorithm.get() == "No Observation":
            self.solution_path, visited_count = no_observation_solve(start_state, goal_state)
        elif self.algorithm.get() == "BFS":
            self.solution_path, visited_count = bfs(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "DFS":
            self.solution_path, visited_count = dfs(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "UCS":
            self.solution_path, visited_count = ucs(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "IDS":
            self.solution_path, visited_count = ids(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Greedy":
            self.solution_path, visited_count = greedy_search(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "A*":
            self.solution_path, visited_count = a_star(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "IDA*":
            self.solution_path, visited_count = ida_star(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Hill Climbing":
            self.solution_path, visited_count = hill_climbing(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Simple Hill":  
            self.solution_path, visited_count = simple_hill_climbing(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Steepest Ascent Hill":
            self.solution_path, visited_count = steepest_ascent_hill_climbing(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Stochastic Hill":
            self.solution_path, visited_count = stochastic_hill_climbing(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Simulated Annealing":
            self.solution_path, visited_count = simulated_annealing(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Genetic Algorithm":
            self.solution_path, visited_count = genetic_algorithm(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Trial and Error":
            self.solution_path, visited_count = trial_and_error(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Beam Search":
            self.solution_path, visited_count = beam_search(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "AND-OR Search":
            self.solution_path, visited_count = and_or_search(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
        elif self.algorithm.get() == "Backtracking CSP":
            self.solution_path, visited_count = backtracking_with_steps(self.start_state, self.goal_state)
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"Visited states: {visited_count}\n")
            self.log_text.insert(tk.END, f"Path length: {len(self.solution_path)}\n")
        elif self.algorithm.get() == "Backtracking - AC-3":
            self.solution_path, visited_count, ac3_log = backtracking_with_ac3(self.start_state, self.goal_state)
            self.log_text.delete(1.0, tk.END)
            # Hiển thị log từ AC-3
            if ac3_log:
                self.log_text.insert(tk.END, "AC-3 Log:\n")
                for log_entry in ac3_log:
                    self.log_text.insert(tk.END, f"{log_entry}\n")
            self.log_text.insert(tk.END, f"Visited states: {visited_count}\n")
            self.log_text.insert(tk.END, f"Path length: {len(self.solution_path)}\n")
        elif self.algorithm.get() == "Q-Learning":
            self.solution_path, visited_count = q_learning(tuple(tuple(row) for row in self.start_state), tuple(tuple(row) for row in self.goal_state))
            
        end_time = time.time()
        runtime = end_time - start_time
        
        # Kiểm tra kết quả cho Partially Observable
        if self.algorithm.get() == "Partially Observable" or self.algorithm.get() == "No Observation":
            if self.solution_path and len(self.solution_path) > 0:
                steps = len(self.solution_path) - 1
                self.log_text.insert(tk.END, f"Solution found!\n")
                self.log_text.insert(tk.END, f"Number of steps: {steps}\n")
                self.log_text.insert(tk.END, f"Time taken: {runtime:.4f} seconds\n")
                self.log_text.insert(tk.END, f"Number of states explored: {visited_count}\n")
                # Thêm kết quả vào bảng so sánh
                self.add_to_comparison(self.algorithm.get(), runtime, visited_count)
                self.animate_solution()
            else:
                self.log_text.insert(tk.END, "No solution found!\n")
                self.log_text.insert(tk.END, f"Time taken: {runtime:.4f} seconds\n")
                self.log_text.insert(tk.END, f"Number of states explored: {visited_count}\n")
        else:
            # Kiểm tra bình thường cho các thuật toán khác
            if self.solution_path:
                final_state = self.solution_path[-1]
                if isinstance(final_state, (list, tuple)) and len(final_state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in final_state):
                    final_flat = [final_state[i][j] for i in range(3) for j in range(3)]
                else:
                    final_flat = final_state
                    
                goal_flat = [self.goal_state[i][j] for i in range(3) for j in range(3)]
                
                if final_flat == goal_flat:
                    steps = len(self.solution_path) - 1
                    self.log_text.insert(tk.END, f"Solution found!\n")
                    self.log_text.insert(tk.END, f"Number of steps: {steps}\n")
                    self.log_text.insert(tk.END, f"Time taken: {runtime:.4f} seconds\n")
                    self.log_text.insert(tk.END, f"Number of states explored: {visited_count}\n")
                    # Thêm kết quả vào bảng so sánh
                    self.add_to_comparison(self.algorithm.get(), runtime, visited_count)
                    self.animate_solution()
                else:
                    self.log_text.insert(tk.END, "No solution found!\n")
                    self.log_text.insert(tk.END, f"Time taken: {runtime:.4f} seconds\n")
                    self.log_text.insert(tk.END, f"Number of states explored: {visited_count}\n")
            else:
                self.log_text.insert(tk.END, "No solution found!\n")
                self.log_text.insert(tk.END, f"Time taken: {runtime:.4f} seconds\n")
                self.log_text.insert(tk.END, f"Number of states explored: {visited_count}\n")
    
    def randomize_start_state(self):
        if self.algorithm.get() == "Backtracking CSP" or self.algorithm.get() == "Backtracking - AC-3":
            messagebox.showerror("Error", "Cannot randomize start state for Backtracking CSP and Backtracking - AC-3")
            return
        import random
        
        if self.algorithm.get() == "Partially Observable" or self.algorithm.get() == "No Observation":
            # Sinh nhiều trạng thái hơn và gần nhau hơn
            num_states = random.randint(3, 5)  # Sinh 3-5 trạng thái
            start_states = []
            goal_states = []
            
            # Sinh trạng thái mục tiêu đầu tiên
            while True:
                goal_state = list(range(9))
                random.shuffle(goal_state)
                goal_matrix = [goal_state[i:i+3] for i in range(0, 9, 3)]
                if is_solvable(goal_matrix):
                    goal_states.append(goal_state)
                    break
            
            # Sinh các trạng thái mục tiêu khác gần với mục tiêu đầu tiên
            for _ in range(num_states - 1):
                current_goal = goal_states[-1].copy()
                # Thực hiện 2-3 bước di chuyển ngẫu nhiên
                for _ in range(random.randint(2, 3)):
                    zero_pos = current_goal.index(0)
                    possible_moves = []
                    if zero_pos >= 3:  # Có thể di chuyển lên
                        possible_moves.append(zero_pos - 3)
                    if zero_pos < 6:  # Có thể di chuyển xuống
                        possible_moves.append(zero_pos + 3)
                    if zero_pos % 3 != 0:  # Có thể di chuyển trái
                        possible_moves.append(zero_pos - 1)
                    if zero_pos % 3 != 2:  # Có thể di chuyển phải
                        possible_moves.append(zero_pos + 1)
                    
                    if possible_moves:
                        swap_pos = random.choice(possible_moves)
                        current_goal[zero_pos], current_goal[swap_pos] = current_goal[swap_pos], current_goal[zero_pos]
                
                goal_states.append(current_goal)
            
            # Sinh trạng thái bắt đầu gần với mục tiêu tương ứng
            for goal_state in goal_states:
                # Tạo trạng thái bắt đầu bằng cách thực hiện 3-5 bước di chuyển ngẫu nhiên
                start_state = goal_state.copy()
                for _ in range(random.randint(3, 5)):
                    zero_pos = start_state.index(0)
                    possible_moves = []
                    if zero_pos >= 3:  # Có thể di chuyển lên
                        possible_moves.append(zero_pos - 3)
                    if zero_pos < 6:  # Có thể di chuyển xuống
                        possible_moves.append(zero_pos + 3)
                    if zero_pos % 3 != 0:  # Có thể di chuyển trái
                        possible_moves.append(zero_pos - 1)
                    if zero_pos % 3 != 2:  # Có thể di chuyển phải
                        possible_moves.append(zero_pos + 1)
                    
                    if possible_moves:
                        swap_pos = random.choice(possible_moves)
                        start_state[zero_pos], start_state[swap_pos] = start_state[swap_pos], start_state[zero_pos]
                
                start_states.append(start_state)
            
            # Cập nhật ô nhập START và GOAL
            self.start_text.delete("1.0", tk.END)
            self.end_text.delete("1.0", tk.END)
            
            for state in start_states:
                self.start_text.insert(tk.END, ",".join(map(str, state)) + "\n")
            for state in goal_states:
                self.end_text.insert(tk.END, ",".join(map(str, state)) + "\n")
            
            # Cập nhật trạng thái hiện tại và vẽ lại
            self.start_state = start_states
            self.goal_state = goal_states
            self.current_state = [start_states[0][i:i+3] for i in range(0, 9, 3)]
            self.draw_puzzle(self.current_state)
            
            self.log_text.insert(tk.END, f"Generated {len(start_states)} random states for Partially/No Observation algorithm.\n")
            self.log_text.insert(tk.END, f"Start states are 3-5 moves away from their corresponding goal states.\n")
            
        else:
            # Logic cũ cho các thuật toán khác
            goal_state = [int(x.strip()) for x in self.end_text.get("1.0", tk.END).split(",")]
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
            self.start_text.delete("1.0", tk.END)
            self.start_text.insert("1.0", ",".join(map(str, start_state)))
            
            # Cập nhật trạng thái hiện tại và vẽ lại
            self.start_state = [start_state[i:i+3] for i in range(0, 9, 3)]
            self.current_state = copy.deepcopy(self.start_state)
            self.draw_puzzle(self.current_state)
            self.log_text.insert(tk.END, f"Random start state generated: {','.join(map(str, start_state))}\n")
        
        # Xóa bảng so sánh
        self.clear_comparison()
        # Cập nhật current_start_str
        self.current_start_str = self.start_text.get("1.0", tk.END).strip()

    def parse_state(self, state_str):
        try:
            # Xử lý nhiều dòng cho belief states
            if self.algorithm.get() == "Partially Observable" or self.algorithm.get() == "No Observation":
                states = []
                for line in state_str.strip().split('\n'):
                    if not line.strip():  # Bỏ qua dòng trống
                        continue
                    nums = [int(x.strip()) for x in line.split(",")]
                    if len(nums) != 9 or set(nums) != set(range(9)):
                        raise ValueError("Invalid input")
                    # Chuyển đổi thành ma trận 3x3
                    state = []
                    for i in range(0, 9, 3):
                        state.append(nums[i:i+3])
                    states.append(state)
                return states
            else:
                # Xử lý bình thường cho các thuật toán khác
                nums = [int(x.strip()) for x in state_str.split(",")]
                if len(nums) != 9 or set(nums) != set(range(9)):
                    raise ValueError("Invalid input")
                return [nums[i:i+3] for i in range(0, 9, 3)]
        except:
            if self.algorithm.get() == "Partially Observable" or self.algorithm.get() == "No Observation":
                messagebox.showerror("Error", "Invalid format for Partially Observable/No Observation.\nPlease enter multiple states, one per line.\nEach line should contain 9 numbers from 0-8, separated by commas.\nExample:\n1,2,3,4,0,5,6,7,8\n1,2,3,4,5,0,6,7,8")
            else:
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
                states = self.solution_path[step]
                # Chuyển đổi trạng thái thành danh sách 3x3 nếu cần
                if isinstance(states, (list, tuple)):
                    if len(states) == 9:  # Nếu là list phẳng
                        state = [list(states[i:i+3]) for i in range(0, 9, 3)]
                    elif isinstance(states[0], (list, tuple)) and len(states) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in states):  # Nếu đã là ma trận 3x3
                        state = [list(row) for row in states]
                    else:  # Nếu là danh sách các trạng thái
                        state = [list(row) for row in states[0]]  # Lấy trạng thái đầu tiên để hiển thị
                else:
                    return
                    
                self.current_state = state
                self.draw_puzzle(state)
                
                # Hiển thị thông tin về các trạng thái hiện tại
                if self.algorithm.get() == "Partially Observable" or self.algorithm.get() == "No Observation":
                    self.log_text.insert(tk.END, f"Step {step}: Showing one of {len(states)} possible states\n")
                
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
                for i, states in enumerate(self.solution_path):
                    if self.algorithm.get() == "Partially Observable" or self.algorithm.get() == "No Observation":
                        # In ra toàn bộ các trạng thái trong belief state
                        self.data_text.insert(tk.END, f"Step {i}: [\n")
                        for s in states:
                            self.data_text.insert(tk.END, f"  {s},\n")
                        self.data_text.insert(tk.END, f"]\n  (One of {len(states)} possible states)\n")
                    else:
                        # Chuyển đổi trạng thái để hiển thị
                        if isinstance(states, (list, tuple)):
                            if len(states) == 9:  # Nếu là list phẳng
                                state = [list(states[j:j+3]) for j in range(0, 9, 3)]
                            elif isinstance(states[0], (list, tuple)) and len(states) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in states):  # Nếu đã là ma trận 3x3
                                state = [list(row) for row in states]
                            else:
                                state = [list(row) for row in states[0]]
                        else:
                            continue
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
        
        # Chuyển đổi state thành ma trận 3x3 nếu cần
        if isinstance(state, (list, tuple)):
            if len(state) == 9:  # Nếu là list phẳng
                state = [state[i:i+3] for i in range(0, 9, 3)]
            elif isinstance(state[0], (list, tuple)) and len(state) == 3 and all(isinstance(row, (list, tuple)) and len(row) == 3 for row in state):  # Nếu đã là ma trận 3x3
                state = state
            else:  # Nếu không phải định dạng hợp lệ
                return
        
        # Then draw the individual cell content
        for i in range(3):
            for j in range(3):
                x0 = j * cell_size + x_offset
                y0 = i * cell_size + y_offset
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                
                # Lấy giá trị từ state và xử lý
                try:
                    value = state[i][j]
                    if isinstance(value, list):
                        if len(value) > 0:
                            value = value[0]
                        else:
                            value = 0
                    
                    try:
                        value = int(value)
                    except (TypeError, ValueError):
                        value = 0
                except (IndexError, TypeError):
                    value = 0
                
                if value is not None and value != 0:
                    # Create shadow
                    self.canvas.create_rectangle(
                        x0 + 3, y0 + 3, 
                        x1 + 3, y1 + 3, 
                        fill="#bbbbbb", outline=""
                    )
                    
                    # Create tile
                    color = self.colors["puzzle_colors"][value-1]
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, 
                        fill=color, outline="#666666", 
                        width=1
                    )
                    
                    # Add number with subtle shadow for 3D effect
                    self.canvas.create_text(
                        (x0+x1)//2 + 1, (y0+y1)//2 + 1, 
                        text=str(value), 
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

    def clear_comparison(self):
        """Xóa tất cả các mục trong bảng so sánh"""
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)

    def add_to_comparison(self, algorithm, time_taken, states_explored):
        """Thêm kết quả vào bảng so sánh"""
        self.comparison_tree.insert("", "end", values=(algorithm, f"{time_taken:.4f}", states_explored))

    def check_state_changed(self):
        """Kiểm tra xem start hoặc goal state có thay đổi không"""
        current_start = self.start_text.get("1.0", tk.END).strip()
        current_goal = self.end_text.get("1.0", tk.END).strip()
        
        if current_start != self.current_start_str or current_goal != self.current_goal_str:
            self.current_start_str = current_start
            self.current_goal_str = current_goal
            self.clear_comparison()
            return True
        return False

    def sort_comparison(self, column):
        """Sắp xếp bảng so sánh theo cột được chọn"""
        # Lấy tất cả các mục
        items = [(self.comparison_tree.set(item, column), item) for item in self.comparison_tree.get_children("")]
        
        # Sắp xếp dựa trên loại dữ liệu
        if column == "Time":
            # Sắp xếp số thực
            items.sort(key=lambda x: float(x[0]))
        elif column == "States":
            # Sắp xếp số nguyên
            items.sort(key=lambda x: int(x[0]))
        else:
            # Sắp xếp chuỗi
            items.sort()
        
        # Sắp xếp lại các mục
        for index, (_, item) in enumerate(items):
            self.comparison_tree.move(item, "", index)
