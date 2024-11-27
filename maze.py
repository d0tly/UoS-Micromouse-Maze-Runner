from typing import Tuple

def create_maze(width: int = 5, height: int = 5):
    return [[[False, False, False, False] for _ in range(width)] for _ in range(height)]

def add_horizontal_wall(maze, x_coordinate, horizontal_line):
    maze[horizontal_line][x_coordinate][2] = True
    maze[horizontal_line-1][x_coordinate][0] = True
    return maze

def add_vertical_wall(maze, y_coordinate, vertical_line):
    maze[y_coordinate][vertical_line][1] = True
    maze[y_coordinate][vertical_line-1][3] = True
    return maze

def get_dimensions(maze) -> Tuple[int, int]:
    return len(maze[0]), len(maze)

def get_walls(maze, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    return maze[y_coordinate][x_coordinate]

