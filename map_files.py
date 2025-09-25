import argparse
import time
from grid_env import GridEnvironment, Agent
from search import uniform_cost_search, a_star_search, local_search_replanning

def main():
    """
    Main function to run the delivery agent project from the command line.
    It handles map loading, algorithm selection, and execution.
    """
    parser = argparse.ArgumentParser(description="Autonomous delivery agent using various search algorithms.")
    parser.add_argument("--map", type=str, required=True, help="Path to the map file (e.g., small_map.txt)")
    parser.add_argument("--planner", type=str, required=True, choices=['ucs', 'a_star', 'dynamic'],
                        help="The planner to use: 'ucs', 'a_star', or 'dynamic' for replanning.")
    
    args = parser.parse_args()

    # Create the environment and agent
    env = GridEnvironment(args.map)
    start_pos = env.get_start_position()
    goal_pos = env.get_goal_position()
    agent = Agent(start_pos)
    
    print(f"Loading map from: {args.map}")
    print(f"Start: {start_pos}, Goal: {goal_pos}")
    print(f"Using planner: {args.planner}")

    path = None
    path_cost = -1
    nodes_expanded = -1
    start_time = time.time()
    
    if args.planner == 'ucs':
        print("\n--- Running Uniform-Cost Search ---")
        path, path_cost, nodes_expanded = uniform_cost_search(env, agent.position, goal_pos)
    elif args.planner == 'a_star':
        print("\n--- Running A* Search ---")
        path, path_cost, nodes_expanded = a_star_search(env, agent.position, goal_pos)
    elif args.planner == 'dynamic':
        print("\n--- Running Dynamic Replanning ---")
        path, path_cost, nodes_expanded = local_search_replanning(env, agent.position, goal_pos)
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Report results
    if path:
        print("\n--- Path Found! ---")
        print(f"Path: {path}")
        print(f"Path Cost: {path_cost}")
        print(f"Nodes Expanded: {nodes_expanded}")
        print(f"Time Taken: {elapsed_time:.4f} seconds")
        print("Final map with path:")
        env.print_grid_with_path(path)
    else:
        print("\n--- No Path Found! ---")
        print(f"Nodes Expanded: {nodes_expanded}")
        print(f"Time Taken: {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    main()