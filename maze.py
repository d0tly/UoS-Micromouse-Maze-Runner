from typing import Tuple

def reflect_indices(x, y, height):
    reflected_y = height - y - 1

    return (x, reflected_y)


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

""""
def updateWalls(runner, L, R, F, wallsMaze):
    orient = get_orientation(runner)
    x = get_x(runner)
    y = get_y(runner)
    
    if L:
        print('left wall here')
        if orient == 0:
            add_vertical_wall(wallsMaze, x-1, y)
        elif orient == 1:
            add_horizontal_wall(wallsMaze, x, y+1)
        elif orient == 2:
            add_vertical_wall(wallsMaze, x, y)
        elif orient == 3:
            add_horizontal_wall(wallsMaze, x, y)
    if R:
        print('right wall here')
        if orient == 0:
            add_vertical_wall(wallsMaze, x, y)
        elif orient == 1:
            add_horizontal_wall(wallsMaze, x, y)
        elif orient == 2:
            add_vertical_wall(wallsMaze, x-1, y)
        elif orient == 3:
            add_horizontal_wall(wallsMaze, x, y+1)
    if F:
        if orient == 0:
            add_horizontal_wall(wallsMaze, x, y+1)
        elif orient == 1:
            add_vertical_wall(wallsMaze, x, y)
        elif orient == 2:
            add_horizontal_wall(wallsMaze, x, y)
        elif orient == 3:
            add_vertical_wall(wallsMaze, x-1, y)
    return wallsMaze
"""

