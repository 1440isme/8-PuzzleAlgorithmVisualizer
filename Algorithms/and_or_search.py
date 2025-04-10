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
    """
    Implements AND-OR search algorithm for the 8-puzzle problem.
    Since 8-puzzle is deterministic, this implementation focuses on the conceptual 
    structure of AND-OR search while adapting it for a deterministic environment.
    """
    def or_search(state, path, visited):
        """OR node: find any one action that leads to success"""
        if state == goal_state:
            return [state], len(visited)
            
        if str(state) in path:  # Check for cycles
            return None, len(visited)
            
        visited.add(str(state))
        
        # Get possible actions (moves)
        blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        # Sort moves by heuristic to try more promising paths first
        move_states = []
        for di, dj, _ in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if str(new_state_tuple) not in visited:
                    h = manhattan_distance(new_state_tuple, goal_state)
                    move_states.append((h, new_state_tuple))
        
        # Sort by heuristic value
        move_states.sort(key=lambda x: x[0])
        
        # Try each action
        for _, new_state_tuple in move_states:
            # For each resulting state, perform AND-search
            result_plan, _ = and_search(new_state_tuple, path + [str(state)], visited)
            
            if result_plan is not None:
                return [state] + result_plan, len(visited)
                    
        return None, len(visited)  # No solution found
    
    def and_search(state, path, visited):
        """AND node: for deterministic problems, this is just passing through to OR-search"""
        # In a deterministic environment like 8-puzzle, AND nodes have only one child
        # So we just pass through to OR-search
        return or_search(state, path, visited)
    
    # Start the AND-OR search
    visited = set()
    plan, visited_count = or_search(initial_state, [], visited)
    
    if plan:
        return plan, visited_count
    else:
        return [], visited_count
