# 8-Puzzle Algorithm Visualizer

A Tkinter-based application to visualize solving the 8-puzzle problem using various search algorithms.

## Features

- Supports multiple algorithms: BFS, DFS, UCS, IDS, and Greedy Best-First Search.
- Interactive GUI with start/goal state input, animation speed control, and step-by-step execution.
- Visual representation of the puzzle and detailed logs.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/1440isme/8-PuzzleAlgorithmVisualizer.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

- Enter the start and goal states as comma-separated numbers (e.g., 1,2,3,4,0,5,6,7,8).
- Select an algorithm (BFS, DFS, UCS, IDS, or Greedy).
- Click "PLAY" to see the solution animation or "Step" to move through it manually.

## Project Structure

- algorithms/: Search algorithm implementations.
- gui/: GUI components using Tkinter.
- models/: Puzzle model and utility functions.
- main.py: Entry point of the application.
