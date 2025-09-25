class GridEnvironment:
    """
    Models the 2D grid city environment.
    Handles map loading, movement costs, and obstacle management.
    """
    def __init__(self, map_file):
        """
        Initializes the grid from a file.
        'S': Start, 'G': Goal, '#': Static Obstacle, 'D': Dynamic Obstacle
        """
        self.grid = self.load_grid(map_file)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.start_pos = None
        self.goal_pos = None
        self.dynamic_obstacles = {}
        self.parse_special_cells()

    def load_grid(self, filename):
        """Loads a grid from a text file."""
        grid = []
        with open(filename, 'r') as f:
            for y, line in enumerate(f):
                row = []
                for x, char in enumerate(line.strip()):
                    if char.isdigit():
                        row.append(int(char))
                    elif char == 'S':
                        row.append(1) # Start is regular terrain
                        self.start_pos = (y, x)
                    elif char == 'G':
                        row.append(1) # Goal is regular terrain
                        self.goal_pos = (y, x)
                    elif char == '#':
                        row.append(float('inf')) # Impassable obstacle
                    elif char == 'D':
                        row.append(1) # Dynamic obstacle starts on regular terrain
                        self.dynamic_obstacles[(y, x)] = True
                    else:
                        row.append(1) # Default terrain cost
                grid.append(row)
        return grid

    def parse_special_cells(self):
        """Identifies start, goal, and dynamic obstacle positions."""
        for r, row in enumerate(self.grid):
            for c, cell_value in enumerate(row):
                if cell_value == 'S':
                    self.start_pos = (r, c)
                elif cell_value == 'G':
                    self.goal_pos = (r, c)
                elif cell_value == 'D':
                    self.dynamic_obstacles[(r, c)] = True

    def get_start_position(self):
        """Returns the start coordinates."""
        return self.start_pos

    def get_goal_position(self):
        """Returns the goal coordinates."""
        return self.goal_pos

    def is_valid(self, pos):
        """Checks if a position is within grid bounds."""
        y, x = pos
        return 0 <= y < self.height and 0 <= x < self.width

    def is_passable(self, pos):
        """Checks if a position is not an obstacle."""
        return self.grid[pos[0]][pos[1]] != float('inf')

    def get_cost(self, pos):
        """Returns the movement cost for a given position."""
        return self.grid[pos[0]][pos[1]]

    def get_neighbors(self, pos):
        """Returns valid and passable 4-connected neighbors."""
        y, x = pos
        neighbors = []
        # 4-connected movement: up, down, left, right
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (y + dy, x + dx)
            if self.is_valid(neighbor_pos) and self.is_passable(neighbor_pos):
                neighbors.append(neighbor_pos)
        return neighbors

    def is_dynamic_obstacle_at(self, pos, time_step):
        """
        Simulates a dynamic obstacle appearing at a specific position and time.
        In this simple example, the dynamic obstacle on the map becomes
        impassable after a certain time step. This is a proof-of-concept.
        """
        if pos in self.dynamic_obstacles and time_step >= 5: # Obstacle appears at step 5
            return True
        return False
        
    def update_grid_with_obstacle(self, pos):
        """Updates the grid to make a dynamic obstacle permanent."""
        if pos in self.dynamic_obstacles:
            self.grid[pos[0]][pos[1]] = float('inf')
    
    def print_grid_with_path(self, path):
        """Prints the grid with the final path marked."""
        display_grid = [row[:] for row in self.grid]
        for y, x in path:
            if display_grid[y][x] != 'S' and display_grid[y][x] != 'G':
                display_grid[y][x] = '*'

        for y, x in path:
            if (y, x) == self.start_pos:
                display_grid[y][x] = 'S'
            elif (y, x) == self.goal_pos:
                display_grid[y][x] = 'G'
            else:
                display_grid[y][x] = '*'
                
        # Handle the start and goal positions specially
        if self.start_pos:
            display_grid[self.start_pos[0]][self.start_pos[1]] = 'S'
        if self.goal_pos:
            display_grid[self.goal_pos[0]][self.goal_pos[1]] = 'G'

        for row in display_grid:
            print(" ".join(map(str, row)))


class Agent:
    """
    Represents the delivery agent.
    """
    def __init__(self, start_pos):
        self.position = start_pos
