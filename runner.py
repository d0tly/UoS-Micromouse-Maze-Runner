from typing import Tuple, Optional,List
import argparse
# ------------------------------
from maze import get_dimensions, get_walls, createInfoMaze
#-----------------------------------------------------------------------------------

def reflect_indices(x, y, height):
    reflected_y = height - y - 1

    return (x, reflected_y)

class Runner:
    def __init__(self, x: int, y: int, orientation: str):
        self.x = x
        self.y = y
        self.real_x = x
        self.real_y = y
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
    elif direction == "Back":
        orientations = {"N": "S", "S": "N", "E": "W", "W": "E"}
        runner.orientation = orientations[runner.orientation]
    return runner

def isAccessible(maze, x, y):
    width, height = get_dimensions(maze)
    return 0 <= x < width and 0 <= y < height

def forward(runner):
    #print(f"Moving forward from ({runner.x}, {runner.y}) facing {runner.orientation}")
    if runner.orientation == "N":
        runner.y += 1
        runner.real_y -= 1
    elif runner.orientation == "S":
        runner.y -= 1
        runner.real_y += 1
    elif runner.orientation == "E":
        runner.x += 1
        runner.real_x += 1
    elif runner.orientation == "W":
        runner.x -= 1
        runner.real_x -= 1
    #print(f"New position: ({runner.x}, {runner.y})")
    return runner

def create_runner(x: int, y: int, orientation: str):
    return Runner(x, y, orientation)

def sense_walls(maze, runner) -> Tuple[bool, bool, bool]:
    if runner.orientation == "N":
        return tuple(maze[runner.real_y][runner.real_x][-1:] + maze[runner.real_y][runner.real_x][:2])
    elif runner.orientation == "E":
        return tuple(maze[runner.real_y][runner.real_x][0:3])
    elif runner.orientation == "S":
        return tuple(maze[runner.real_y][runner.real_x][1:4])
    elif runner.orientation == "W":
        return tuple(maze[runner.real_y][runner.real_x][2:] + maze[runner.real_y][runner.real_x][:1])


def go_straight(runner, maze):
    if not sense_walls(maze, runner)[1]:
        runner = forward(runner)
        return runner
    else:
        print(f"Cannot go straight from {runner.x}, {runner.y}, {runner.orientation}")
        raise ValueError("Cannot go straight")

def manhattan_distance(maze, goal):
    width, height = len(maze[0]), len(maze)
    distanceMaze = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            distanceMaze[y][x] = abs(goal[0] - x) + abs(goal[1] - y)
    return distanceMaze

def findSmallestDistance(x, y, maze, infoMaze):
    check = get_walls(maze, x, y)
    smallest = []
    moves = {
        0: (0, 1),  
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0)
    }
    for i in range(4):
        if not check[i]:
            xNum, yNum = moves[i]
            coordX = x + xNum
            coordY = y + yNum
            if isAccessible(maze, coordX, coordY):
                smallest.append([(coordX, coordY), infoMaze[coordY][coordX][1]])

    return min(smallest, key=lambda x: x[1])[1]
    
def floodfill(goal, maze, infoMaze):
    queue = []
    queue.append(goal)
    width, height = get_dimensions(maze)
    debug = False
    isChecked = [[0 for _ in range(width)] for _ in range(height)]
    count = 0 
    while all(all(row) for row in isChecked) < 3 and len(queue) > 0:
        count += 1
        x, y = queue.pop(0)

        check = get_walls(maze, x, y)
        moves = {
            0: (0, 1),  
            1: (1, 0),
            2: (0, -1),
            3: (-1, 0)
        }  
        for i in range(4):
            if not check[i]:
                xNum, yNum = moves[i]
                coordX = x + xNum
                coordY = y + yNum
                if isAccessible(maze, coordX, coordY) and isChecked[coordY][coordX] == False:
                    isChecked[coordY][coordX] += 1
                    value = findSmallestDistance(coordX, coordY, maze, infoMaze) + 1
                    if value < infoMaze[coordY][coordX][1]:
                        infoMaze[coordY][coordX][1] = value
                    queue.append((coordX, coordY))
            
    return infoMaze[::-1]

def move(runner, maze, infoMaze):
    x = runner.real_x
    y = runner.real_y
    if get_walls(maze, x, y) == (True, True, True, True):
        return 'False'
    orient = runner.orientation
    L = sense_walls(maze, runner)[0]
    R = sense_walls(maze, runner)[2]
    F = sense_walls(maze, runner)[1]
    
    decisionQueue = []
    
    moves = {
        'N': [[(-1, 0),'Left'], [(0, -1),'Forward'], [(1, 0),'Right']],  
        'E': [[(0, -1),'Left'], [(1, 0),'Forward'], [(0, 1),'Right']],  
        'S': [[(1, 0),'Left'], [(0, 1),'Forward'], [(-1, 0),'Right']], 
        'W': [[(0, 1),'Left'], [(-1, 0),'Forward'], [(0, -1),'Right']]  
    }
    
    for i in range(3):
        xNum, yNum = moves[orient][i][0]
        coordX = x + xNum
        coordY = y + yNum
        if not [L, F, R][i]:
            if isAccessible(maze, coordX, coordY):
                decisionQueue.append([(coordX, coordY), infoMaze[coordY][coordX][0], infoMaze[coordY][coordX][1], moves[orient][i][1]])
        
    if len(decisionQueue) == 0:
        return "Back"
    
    direction = min(decisionQueue, key=lambda x: x[2])[3]
    
    return direction

def explore(runner, maze, goal : Optional[Tuple[int, int]], mazeFile) -> str:
    infoMaze = createInfoMaze(maze, goal)
    infoMaze = floodfill(goal, maze, infoMaze)
    runner.real_x, runner.real_y = reflect_indices(runner.x, runner.y, len(maze))
    answer = ''

    while True:
        direction = move(runner, maze, infoMaze)
        
        if direction == "Forward":
            runner = go_straight(runner, maze)
            answer += 'F'
            
        if direction == "Left" or direction == "Right":
            answer += direction[0]
            runner = turn(runner, direction)
            answer += 'F'
            
        
        if direction == "Back":
            answer += 'B'
            runner = turn(runner, "Back")
                
        if (runner.real_x, runner.real_y) == reflect_indices(goal[0],goal[1],len(maze)):
            return answer