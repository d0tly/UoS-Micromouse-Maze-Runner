from typing import Tuple, Optional, List
from collections import deque
from maze import create_maze, get_dimensions, get_walls, add_horizontal_wall, add_vertical_wall

class Runner:
    def __init__(self, x: int, y: int, orientation: str):
        self.x = x
        self.y = y
        self.orientation = orientation

def get_x(runner):
    return runner.x

def get_y(runner):
    return runner.y

def get_orientation(runner):
    return runner.orientation

def turn(runner, direction: str):
    if direction == "Left":
        orientations = {"N": "W", "W": "S", "S": "E", "E": "N"}
        runner.orientation = orientations[runner.orientation]
    elif direction == "Right":
        orientations = {"N": "E", "E": "S", "S": "W", "W": "N"}
        runner.orientation = orientations[runner.orientation]
    return runner

def forward(runner, width, height):
    print(f"Moving forward from ({runner.x}, {runner.y}) facing {runner.orientation}")
    if runner.orientation == "N" and runner.y > 0:
        runner.y -= 1
    elif runner.orientation == "S" and runner.y < height - 1:
        runner.y += 1
    elif runner.orientation == "E" and runner.x < width - 1:
        runner.x += 1
    elif runner.orientation == "W" and runner.x > 0:
        runner.x -= 1
    print(f"New position: ({runner.x}, {runner.y})")
    return runner

def create_runner(x: int, y: int, orientation: str):
    return Runner(x, y, orientation)

def sense_walls(maze, runner) -> Tuple[bool, bool, bool]:
    if runner.orientation == "N":
        return tuple(get_walls(maze, runner.x, runner.y)[-1:] + get_walls(maze, runner.x, runner.y)[:2])
    elif runner.orientation == "E":
        return tuple(get_walls(maze, runner.x, runner.y)[:3])
    elif runner.orientation == "S":
        return tuple(get_walls(maze, runner.x, runner.y)[1:4])
    elif runner.orientation == "W":
        return tuple(get_walls(maze, runner.x, runner.y)[2:] + get_walls(maze, runner.x, runner.y)[:1])

def go_straight(runner, maze):
    width, height = get_dimensions(maze)
    if not sense_walls(maze, runner)[1]:
        forward(runner, width, height)
        return runner
    else:
        print(f"Cannot go straight from {runner.x}, {runner.y}, {runner.orientation}")
        raise ValueError("Cannot go straight")

def bfs_update_distances(maze, goal):
    width, height = get_dimensions(maze)
    distanceMaze = [[float('inf')] * width for _ in range(height)]
    queue = deque([goal])
    distanceMaze[goal[1]][goal[0]] = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # N, E, S, W

    while queue:
        x, y = queue.popleft()
        current_distance = distanceMaze[y][x]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and distanceMaze[ny][nx] == float('inf'):
                if not maze[ny][nx][directions.index((-dx, -dy))]:  # Check if there's no wall in the opposite direction
                    distanceMaze[ny][nx] = current_distance + 1
                    queue.append((nx, ny))

    return distanceMaze

def move(runner, maze, distanceMaze, goal) -> str:
    check = sense_walls(maze, runner)
    distanceCheck = []

    moves = {
        "N": [(0, 1), (1, 0), (-1, 0)],
        "E": [(1, 0), (0, -1), (0, 1)],
        "S": [(0, -1), (-1, 0), (1, 0)],
        "W": [(-1, 0), (0, 1), (0, -1)]
    }
    
    orientation = get_orientation(runner)
    width, height = get_dimensions(maze)
    
    for i in range(3):
        x, y = moves[orientation][i]
        new_x = get_x(runner) + x
        new_y = get_y(runner) + y
        if 0 <= new_x < width and 0 <= new_y < height:
            if not check[i]:
                distanceCheck.append(distanceMaze[new_y][new_x])
            else:
                distanceCheck.append(float("inf"))
                if orientation == "N":
                    add_horizontal_wall(maze, get_x(runner), get_y(runner))
                elif orientation == "E":
                    add_vertical_wall(maze, get_x(runner), get_y(runner))
                elif orientation == "S":
                    add_horizontal_wall(maze, get_x(runner), get_y(runner) - 1)
                elif orientation == "W":
                    add_vertical_wall(maze, get_x(runner) - 1, get_y(runner))
                # Recalculate distances after adding a wall
                distanceMaze = bfs_update_distances(maze, goal)
        else:
            distanceCheck.append(float("inf"))
    
    min_index = distanceCheck.index(min(distanceCheck))
    if min_index == 0:
        print(f"Turning Left from ({runner.x}, {runner.y}) facing {runner.orientation}")
        turn(runner, "Left")
    elif min_index == 1:
        print(f"Going Straight from ({runner.x}, {runner.y}) facing {runner.orientation}")
        go_straight(runner, maze)
    elif min_index == 2:
        print(f"Turning Right from ({runner.x}, {runner.y}) facing {runner.orientation}")
        turn(runner, "Right")
    
    return orientation

def explore(runner, maze, goal: Optional[Tuple[int, int]] = None) -> str:
    if goal is None:
        goal = (get_dimensions(maze)[0] - 1, get_dimensions(maze)[1] - 1)
        
    distanceMaze = bfs_update_distances(maze, goal)
    
    resultingCombination = ''
    
    while (get_x(runner), get_y(runner)) != goal:
        print(runner.x, runner.y, runner.orientation)
        resultingCombination += move(runner, maze, distanceMaze, goal)
    
    return resultingCombination

def convert_maze(text_maze):
    height = len(text_maze)
    width = len(text_maze[0])
    maze = create_maze(width, height)
    
    for y in range(height):
        for x in range(width):
            if text_maze[y][x] == '#':
                if y > 0 and text_maze[y-1][x] == '#':
                    add_horizontal_wall(maze, x, y)
                if x < width - 1 and text_maze[y][x+1] == '#':
                    add_vertical_wall(maze, y, x)
    return maze

# Provided maze
text_maze = [
    "###########",
    "#...#.....#",
    "#.###.###.#",
    "#...#...#.#",
    "#.#.#.#####",
    "#.#...#...#",
    "#####.#.###",
    "#.#...#...#",
    "#.#.###.#.#",
    "#.......#.#",
    "###########"
]

# Convert the maze
maze = convert_maze(text_maze)

# Initialize the runner
runner = Runner(1, 1, "N")

# Set the goal
goal = (9, 9)

# Run the exploration
result = explore(runner, maze, goal)
print(result)