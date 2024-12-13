from typing import Tuple, Optional,List
import argparse
# ------------------------------

def reflect_indices(x, y, height):
    reflected_y = height - y - 1

    return (x, reflected_y)

def maze_reader(maze_file: str):
    try:
        with open(maze_file, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        raise IOError(f"error read maze file {e}")

    maze = [line.strip() for line in lines]
    if not maze:
        raise ValueError("maze file empty")

    width = len(maze[0])
    if any(len(row) != width for row in maze):
        raise ValueError("maze rows not same width")

    for i, row in enumerate(maze):
        if not all(c in {'#', '.'} for c in row):
            raise ValueError(f"bad character in maze row {i} {row}")
        if i == 0 or i == len(maze) - 1:
            if not all(c == '#' for c in row):
                raise ValueError(f"top or bottom row not all walls {row}")
        else:
            if row[0] != '#' or row[-1] != '#':
                raise ValueError(f"row {i} not all walls {row}")

    lines = ''
    
    try:
        with open(maze_file, 'r') as file:
            lines = file.read()
    except Exception as e:
        raise IOError(f"error read maze file {e}")
            
    text = lines.strip().split('\n')
    textMaze = [list(line) for line in text]
    rows = len(textMaze)
    cols = len(textMaze[0])
    maze = create_maze(int((len(textMaze[0])-1)/2), int((len(textMaze) - 1)/2))
    for y in range(rows):
        if y % 2 != 0:
            for x in range(cols):
                if x % 2 != 0 and x != 0 and x != cols - 1:
                    coordX, coordY = int((x-1)/2), int((y-1)/2)
            
                    if textMaze[y-1][x] == "#":
                        maze = add_horizontal_wall_reader(maze, coordX, coordY-1)
                    if textMaze[y+1][x] == "#":
                        maze = add_horizontal_wall_reader(maze, coordX, coordY)
                    if textMaze[y][x+1] == "#":
                        maze = add_vertical_wall_reader(maze, coordY, coordX+1)
                    if textMaze[y][x-1] == "#":
                        maze = add_vertical_wall_reader(maze, coordY, coordX)
    return maze


def validate_position(position: str, maze, name: str):
    try:
        x, y = map(int, position.split(','))
    except ValueError:
        raise ValueError(f"bad format for {name} must be x y format")

    if y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]):
        raise ValueError(f"{name} position {x} {y} out of maze bounds")
    return x, y

def parseArgs():
    parser = argparse.ArgumentParser(description="ECS Maze Runner")
    parser.add_argument("maze", help="The name of the maze file, e.g., maze1.mz")
    parser.add_argument("--starting", help="The starting position, e.g., '2, 1'", required=True)
    parser.add_argument("--goal", help="The goal position, e.g., '4, 5'", required=True)

    args = parser.parse_args()

    try:
        maze = maze_reader(args.maze)
    except (IOError, ValueError) as e:
        print(f"error broski {e}")
        return

    try:
        start = validate_position(args.starting, maze, "start")
        goal = validate_position(args.goal, maze, "goal")
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("Maze:")
    for row in maze:
        print(row)
    print(f"\nstarting pos{start}")
    print(f"goal pos{goal}")

    exploration_steps, path = explore_maze(maze, start, goal, args.maze)
    write_statistics(args.maze, exploration_steps, path)

def explore_maze(maze, start, goal, maze_file):
    runner = create_runner(start[0], start[1], "N")
    infoMaze = createInfoMaze(maze, goal)
    infoMaze = floodfill(goal, maze, infoMaze)
    exploration_steps = 0
    path = []
    path.append((get_x(runner), get_y(runner)))
    actions = []
    
    with open("exploration.csv", "w", newline="") as csvfile:
        fieldnames = ["Step", "x-coordinate", "y-coordinate", "Actions"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        count = 0
        
        while True:
            direction = move(runner, maze, infoMaze)
            if direction == "Forward":
                runner = go_straight(runner, maze)
                actions.append("F")
            elif direction == "Left" or direction == "Right":
                actions.append(direction[0])
                runner = turn(runner, direction)
                runner = go_straight(runner, maze)
                actions.append("F")
            elif direction == "Back":
                actions.append("B")
                runner = turn(runner, "Back")
            
            path.append()
            
            exploration_steps += 1
            writer.writerow({"Step": exploration_steps, "x-coordinate": path[count][0], "y-coordinate": path[count][1], "Actions": "".join(actions)})
            count += 1
            actions = []
            
            path.append((get_x(runner), get_y(runner)))
            
            if (runner.x, runner.y) == goal:
                writer.writerow({"Step": exploration_steps, "x-coordinate": path[count][0], "y-coordinate": path[count][1], "Actions": "".join(actions)})
                break
    
    return exploration_steps, path

def write_statistics(maze_file, exploration_steps, path):
    path_length = len(path)
    score = exploration_steps / 4 + path_length
    
    with open("statistics.txt", "w") as file:
        file.write(f"{maze_file}\n")
        file.write(f"{score}\n")
        file.write(f"{exploration_steps}\n")
        file.write(f"{path}\n")
        file.write(f"{path_length}\n")

def main():
    parseArgs()

    
    
def convert_to_grid_format(maze_file, runner):
    text = ''
    try:
        with open(maze_file, 'r') as file:
            text = file.read()  
    except Exception as e:
        raise IOError(f"Error reading maze file: {e}")
    
    lines = text.strip().split('\n')
    maze = [list(line) for line in lines]
    rows = len(maze)
    cols = len(maze[0])
    grid = []
    x = runner.real_x
    y = runner.real_y
    orient = get_orientation(runner)
    
    for i in range(rows):
        row = []
        if i % 2 == 0:
            for j in range(cols):
                if j % 2 == 0:
                    row.append('o')
                else:
                    if maze[i][j] == "#":
                        row.append("---")
                    else:
                        row.append("   ")
        else:
            for j in range(cols):
                if j % 2 == 0:
                    if maze[i][j] == "#":
                        row.append("|")
                    else:
                        row.append(" ")
                else:
                    if i == (y*2)+1 and j == (x*2)+1:
                        if orient == 'N':
                            row.append(" ^ ")
                        elif orient == 'E':
                            row.append(" > ")
                        elif orient == 'S':
                            row.append(" v ")
                        elif orient == 'W':
                            row.append(" < ")
                    else:
                        row.append("   ")
        grid.append(row)
                        
    
    return grid
#-----------------------------------------------------------------------------------
from typing import Tuple

def create_maze(width: int = 5, height: int = 5):
    maze = [[[False, False, False, False] for _ in range(width)] for _ in range(height)]
    
    return maze

def createInfoMaze(maze, goal):
    width, height = get_dimensions(maze)
    # [isVisited, distance]
    result = [[[False, 1000] for _ in range(width)] for _ in range(height)]
    result[goal[1]][goal[0]] = [False, 0] 
    return result


def add_vertical_wall(maze, y_coordinate, vertical_line):
    vertical_line, y_coordinate = reflect_indices(vertical_line, y_coordinate, len(maze))
    
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line < len(maze[0]):
        maze[y_coordinate][vertical_line][3] = True
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line - 1 < len(maze[0]):
        maze[y_coordinate][vertical_line-1][1] = True
    return maze

def add_horizontal_wall(maze, x_coordinate, horizontal_line):
    x_coordinate, horizontal_line = reflect_indices(x_coordinate, horizontal_line, len(maze))
    
    if 0 <= horizontal_line < len(maze) and 0 <= x_coordinate < len(maze[0]):
            maze[horizontal_line][x_coordinate][2] = True
    if 0 <= horizontal_line + 1 < len(maze) and 0 <= x_coordinate < len(maze[0]):
            maze[horizontal_line+1][x_coordinate][0] = True
    return maze

def add_vertical_wall_reader(maze, y_coordinate, vertical_line):
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line < len(maze[0]):
        maze[y_coordinate][vertical_line][3] = True
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line - 1 < len(maze[0]):
        maze[y_coordinate][vertical_line-1][1] = True
    return maze

def add_horizontal_wall_reader(maze, x_coordinate, horizontal_line):
    if 0 <= horizontal_line < len(maze) and 0 <= x_coordinate < len(maze[0]):
            maze[horizontal_line][x_coordinate][2] = True
    if 0 <= horizontal_line + 1 < len(maze) and 0 <= x_coordinate < len(maze[0]):
            maze[horizontal_line+1][x_coordinate][0] = True
    return maze

def get_dimensions(maze) -> Tuple[int, int]:
    return len(maze[0]), len(maze)

def get_walls(maze, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    x_coordinate, y_coordinate = reflect_indices(x_coordinate, y_coordinate, len(maze))
    return tuple(maze[y_coordinate][x_coordinate])
#-----------------------------------------------------------------------------------

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

    result = convert_to_grid_format(mazeFile, runner)
    for row in result:
        print("".join(str(cell) for cell in row))

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
            result = convert_to_grid_format(mazeFile, runner)
            for row in result:
                print("".join(str(cell) for cell in row))
            for row in infoMaze:
                print(" ".join(
                    f"  {cell[1]}" if len(str(cell[1])) == 1 else
                    f" {cell[1]}" if len(str(cell[1])) == 2 else
                    str(cell[1])
                    for cell in row
                ))
            print(answer)
            return answer
    
def shortest_path(maze, start: Optional[Tuple[int, int]] = (0,0), goal: Optional[Tuple[int, int]] = (0,0)) -> List[Tuple[int, int]]:
    if goal == (0,0):
        goal = (len(maze[0]) - 1, len(maze) - 1)
    runner = create_runner(start[0], start[1], "N")
    infoMaze = createInfoMaze(maze, goal)
    infoMaze = floodfill(goal, maze, infoMaze)
    runner.real_x, runner.real_y = reflect_indices(runner.x, runner.y, len(maze))
    answer = []
    answer.append((get_x(runner), get_y(runner)))
    
    while True:
        direction = move(runner, maze, infoMaze)
        
        if direction == "Forward":
            runner = go_straight(runner, maze)
            answer.append((get_x(runner), get_y(runner)))

        if direction == "Left" or direction == "Right":
            runner = turn(runner, direction)
            
            runner = go_straight(runner, maze)
            answer.append((get_x(runner), get_y(runner)))
            
            
        
        if direction == "Back":
            runner = turn(runner, direction)

                
        if (runner.real_x, runner.real_y) == reflect_indices(goal[0],goal[1],len(maze)):
            print(answer)
            return answer
            

maze = maze_reader("doom_maze.mz")
Runner = create_runner(0, 0, "N")
explore(Runner, maze, (99, 49), "doom_maze.mz")
