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

def isAccessible(maze, x, y):
    width, height = get_dimensions(maze)
    return 0 <= x < width and 0 <= y < height

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

def manhattan_distance(maze, goal):
    width, height = get_dimensions(maze)
    distanceMaze = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            distanceMaze[y][x] = abs(goal[0] - x) + abs(goal[1] - y)
    return distanceMaze

def move(runner, maze, goal, isVisitedMaze) -> str:
    check = sense_walls(maze, runner)
    decisionQueue = []
    
    moves = {
        "N": [[(-1, 0),'Left'], [(0, 1),'Forward'], [(1, 0),'Right']],
        "E": [[(0, 1),'Left'], [(1, 0),'Forward'], [(0, -1),'Right']],
        "S": [[(1, 0),'Left'], [(0, -1),'Forward'], [(-1, 0),'Right']],
        "W": [[(0, -1),'Left'], [(-1, 0),'Forward'], [(0, 1),'Right']]
    }
    
    for i in range(3):
            if check[i] == False:
                        xNum, yNum = moves[get_orientation(runner)][i]
                        coordX = get_x(runner) + xNum
                        coordY = get_y(runner) + yNum
                        if isAccessible(maze, coordX, coordY):
                            decisionQueue.append([(coordX, coordY), isVisitedMaze[coordY][coordX], distanceMaze[coordY][coordX]], moves[get_orientation(runner)][i][1])
    
    
    if len(decisionQueue) == 0:
        turn(runner, 'Right')
        turn(runner, 'Right')
        return 'RR'
    else:
              
                            
            
    return orientation

def explore(runner, maze, goal: Optional[Tuple[int, int]] = None) -> str:
    if goal is None:
        goal = (get_dimensions(maze)[0] - 1, get_dimensions(maze)[1] - 1)
    
    visitedQueue = []
    distanceMaze = manhattan_distance(maze, goal)
    isVisitedMaze = [[False for _ in range(get_dimensions(maze)[0])] for _ in range(get_dimensions(maze)[1])]
    
    while (get_x(runner), get_y(runner)) != goal:
        print(runner.x, runner.y, runner.orientation)
        move(runner, maze, goal, isVisitedMaze)
    
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