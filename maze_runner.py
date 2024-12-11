import argparse
import os
import csv
from typing import List, Optional, Tuple
from runner import create_runner, get_x, get_y, turn, forward, get_orientation, go_straight, move, floodfill
from maze import create_maze, add_horizontal_wall, add_vertical_wall, createInfoMaze

def reflect_indices(x, y, height):
    reflected_y = height - 1 - y

    return (x // 2, reflected_y)

def shortest_path(maze, start: Optional[Tuple[int, int]] = (0,0), goal: Optional[Tuple[int, int]] = (0,0)) -> List[Tuple[int, int]]:
    if goal == (0,0):
        goal = (len(maze[0]) - 1, len(maze) - 1)
    runner = create_runner(start[0], start[1], "N")
    infoMaze = createInfoMaze(maze, goal)
    infoMaze = floodfill(goal, maze, infoMaze)
    answer = []
    answer.append((get_x(runner), get_y(runner)))
    
    while True:
        direction = move(runner, maze, infoMaze)
        if direction == "Forward":
            runner = go_straight(runner, maze)
            
        if direction == "Left" or direction == "Right":
            runner = turn(runner, direction)
            runner = go_straight(runner, maze)
        
        if direction == "Back":
            runner = turn(runner, "Back")
        
        answer.append((get_x(runner), get_y(runner)))
        if (runner.x, runner.y) == goal:
            print(answer)
            return answer
        

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
                    if y + 1 < rows and textMaze[y+1][x] == "#":
                        maze = add_horizontal_wall(maze, coordX, coordY+1)
                    if y - 1 >= 0 and textMaze[y-1][x] == "#":
                        maze = add_horizontal_wall(maze, coordX, coordY)
                    if x + 1 < cols and textMaze[y][x+1] == "#":
                        maze = add_vertical_wall(maze, coordY, coordX+1)
                    if x - 1 >= 0 and textMaze[y][x-1] == "#":
                        maze = add_vertical_wall(maze, coordY, coordX)
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
    x = get_x(runner)
    y = get_y(runner)
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

if __name__ == "__main__":
    main()
    
    
