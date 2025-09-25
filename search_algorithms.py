import heapq
import random

def uniform_cost_search(environment, start_pos, goal_pos):
    """
    Uniform-Cost Search (UCS) implementation.
    Explores the grid to find the least-cost path from start to goal.
    Returns the path, its cost, and the number of nodes expanded.
    """
    # Priority queue stores tuples of (cost, position, path_list)
    frontier = [(0, start_pos, [start_pos])]
    # Visited set to prevent cycles and redundant work
    visited = {start_pos: 0}
    nodes_expanded = 0

    while frontier:
        cost, current_pos, path = heapq.heappop(frontier)
        nodes_expanded += 1

        if current_pos == goal_pos:
            return path, cost, nodes_expanded

        for next_pos in environment.get_neighbors(current_pos):
            move_cost = environment.get_cost(next_pos)
            new_cost = cost + move_cost
            
            # If the neighbor is not visited or a cheaper path is found
            if next_pos not in visited or new_cost < visited[next_pos]:
                visited[next_pos] = new_cost
                new_path = path + [next_pos]
                heapq.heappush(frontier, (new_cost, next_pos, new_path))
    
    return None, -1, nodes_expanded

def manhattan_distance(pos1, pos2):
    """
    Calculates the Manhattan distance heuristic.
    It's the sum of the absolute differences of the coordinates.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def a_star_search(environment, start_pos, goal_pos):
    """
    A* Search implementation with Manhattan distance as the heuristic.
    Returns the path, its cost, and the number of nodes expanded.
    """
    # Priority queue stores tuples of (f_cost, g_cost, position, path_list)
    frontier = [(0 + manhattan_distance(start_pos, goal_pos), 0, start_pos, [start_pos])]
    # Visited set stores the minimum g_cost to reach a position
    visited = {start_pos: 0}
    nodes_expanded = 0

    while frontier:
        f_cost, g_cost, current_pos, path = heapq.heappop(frontier)
        nodes_expanded += 1

        if current_pos == goal_pos:
            return path, g_cost, nodes_expanded

        for next_pos in environment.get_neighbors(current_pos):
            move_cost = environment.get_cost(next_pos)
            new_g_cost = g_cost + move_cost

            if next_pos not in visited or new_g_cost < visited[next_pos]:
                visited[next_pos] = new_g_cost
                new_f_cost = new_g_cost + manhattan_distance(next_pos, goal_pos)
                new_path = path + [next_pos]
                heapq.heappush(frontier, (new_f_cost, new_g_cost, next_pos, new_path))

    return None, -1, nodes_expanded

def local_search_replanning(environment, start_pos, goal_pos, max_steps=1000):
    """
    A simple local search replanning strategy.
    It uses A* to find an initial path, then monitors it.
    If a dynamic obstacle appears on the path, it replans from the agent's current position.
    This demonstrates the dynamic replanning concept.
    """
    print("Initial planning with A*...")
    path, path_cost, nodes_expanded = a_star_search(environment, start_pos, goal_pos)
    
    if not path:
        return None, -1, nodes_expanded

    print("Initial path found. Starting agent movement...")
    
    total_path_cost = 0
    total_nodes_expanded = nodes_expanded

    for i in range(len(path) - 1):
        current_pos = path[i]
        
        # Simulate moving to the next position
        next_pos = path[i+1]
        
        # A simple check to simulate a dynamic obstacle appearing
        # This will be triggered on the 'dynamic_map.txt'
        if environment.is_dynamic_obstacle_at(next_pos, i+1):
            print(f"\nDYNAMIC OBSTACLE DETECTED at {next_pos}!")
            print("Initiating replanning from current position...")
            
            # Simulate the environment update
            environment.update_grid_with_obstacle(next_pos)
            
            # Use A* to find a new path from the current position
            new_path, new_cost, new_expanded = a_star_search(environment, current_pos, goal_pos)
            
            if new_path:
                print("New path found!")
                path = path[:i] + new_path # Update the path
                total_path_cost += new_cost
                total_nodes_expanded += new_expanded
                i = -1 # Restart the loop from the beginning of the new path
            else:
                print("Could not find a new path. Agent is stuck.")
                return None, -1, total_nodes_expanded
        
        total_path_cost += environment.get_cost(next_pos)
    
    return path, total_path_cost, total_nodes_expanded
