import API
import sys
from typing import Tuple

x=0
y=0
orient=0
cell = 0

cells = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

flood=[[14,13,12,11,10,9,8,7,7,8,9,10,11,12,13,14],
        [13,12,11,10,9,8,7,6,6,7,8,9,10,11,12,13],
        [12,11,10,9,8,7,6,5,5,6,7,8,9,10,11,12],
        [11,10,9,8,7,6,5,4,4,5,6,7,8,9,10,11],
        [10,9,8,7,6,5,4,3,3,4,5,6,7,8,9,10],
        [9,8,7,6,5,4,3,2,2,3,4,5,6,7,8,9],
        [8,7,6,5,4,3,2,1,1,2,3,4,5,6,7,8],
        [7,6,5,4,3,2,1,0,0,1,2,3,4,5,6,7],
        [7,6,5,4,3,2,1,0,0,1,2,3,4,5,6,7],
        [8,7,6,5,4,3,2,1,1,2,3,4,5,6,7,8],
        [9,8,7,6,5,4,3,2,2,3,4,5,6,7,8,9],
        [10,9,8,7,6,5,4,3,3,4,5,6,7,8,9,10],
        [11,10,9,8,7,6,5,4,4,5,6,7,8,9,10,11],
        [12,11,10,9,8,7,6,5,5,6,7,8,9,10,11,12],
        [13,12,11,10,9,8,7,6,6,7,8,9,10,11,12,13],
        [14,13,12,11,10,9,8,7,7,8,9,10,11,12,13,14]]

flood2= [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

returnMaze = [[1000 for _ in range(16)] for _ in range(16)]
#done
def orientation(orient,turning):
    if (turning== 'L'):
        orient-=1
        if (orient==-1):
            orient=3
    elif(turning== 'R'):
        orient+=1
        if (orient==4):
            orient=0
    elif(turning== 'B'):
        if (orient==0):
            orient=2
        elif (orient==1):
            orient=3
        elif (orient==2):
            orient=0
        elif (orient==3):
            orient=1

    return(orient)
#done
def updateCoordinates(x,y,orient):

    if (orient==0):
        y+=1
    if (orient==1):
        x+=1
    if (orient==2):
        y-=1
    if (orient==3):
        x-=1

    return(x,y)

def manhattan_distance(maze, goal):
    width, height = len(maze[0]), len(maze)
    distanceMaze = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            distanceMaze[y][x] = abs(goal[0] - x) + abs(goal[1] - y)
    return distanceMaze

def checkCell(x, y, maze):
    if maze[y][x] == 1000:
        return -1
    else:
        return 1


def create_maze(width: int = 5, height: int = 5):
    return [[[False, False, False, False] for _ in range(width)] for _ in range(height)]

def add_horizontal_wall(maze, x_coordinate, horizontal_line):
    if 0 <= horizontal_line < len(maze) and 0 <= x_coordinate < len(maze[0]):
        if maze[horizontal_line][x_coordinate][2] != True:
            print(f"Adding horizontal wall at ({x_coordinate}, {horizontal_line})")
            maze[horizontal_line][x_coordinate][2] = True
    if 0 <= horizontal_line - 1 < len(maze) and 0 <= x_coordinate < len(maze[0]):
        if maze[horizontal_line-1][x_coordinate][0] != True:
            print(f"Adding horizontal wall at ({x_coordinate}, {horizontal_line-1})")
            maze[horizontal_line-1][x_coordinate][0] = True
    return maze

def add_vertical_wall(maze, vertical_line, y_coordinate):
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line < len(maze[0]):
        if maze[y_coordinate][vertical_line][1] != True:
            print(f"Adding vertical wall at ({vertical_line}, {y_coordinate})")
            maze[y_coordinate][vertical_line][1] = True
    else:
        print(f"Out of bounds vertical wall to the right at ({vertical_line}, {y_coordinate})")
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line + 1 < len(maze[0]):
        if maze[y_coordinate][vertical_line+1][3] != True:
            print(f"Adding vertical wall at ({vertical_line+1}, {y_coordinate})")
            maze[y_coordinate][vertical_line+1][3] = True
    else:
        print(f"Out of bounds vertical wall to the left at ({vertical_line+1}, {y_coordinate})")

def updateWalls(x, y, orient, L, R, F, wallsMaze):
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

def get_dimensions(maze) -> Tuple[int, int]:
    return len(maze[0]), len(maze)

def get_walls(maze, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    return maze[y_coordinate][x_coordinate]

def sense_walls(maze, x,y) -> tuple[bool, bool, bool,bool]:
    return tuple(get_walls(maze, x,y))

def findSmallestDistance(x, y, wallsMaze, isVisitedMaze, returnMaze):
    check = sense_walls(wallsMaze, x, y)
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
            if 0 <= coordX < 16 and 0 <= coordY < 16 and isVisitedMaze[coordY][coordX] and cells[coordY][coordX] == 0:
                smallest.append([(coordX, coordY), returnMaze[coordY][coordX]])

    return min(smallest, key=lambda x: x[1])[1]
            
def check_visited_coordinates(isVisitedMaze, returnMaze):
    for y in range(len(isVisitedMaze)):
        for x in range(len(isVisitedMaze[0])):
            if isVisitedMaze[y][x] and returnMaze[y][x] == 1000:
                return False
    return True
    
def floodfill(startX, startY, isVisitedMaze, returnMaze, wallsMaze,state = False):
    queue = [(startX, startY)]

    for y in range(3):
        while not check_visited_coordinates(isVisitedMaze, returnMaze):
            print(returnMaze)
            if len(queue) == 0:
                return returnMaze
            x, y = queue.pop(0)
            check = sense_walls(wallsMaze, x, y)
            moves = {
                0: [(0, 1)],  
                1: [(1, 0)],
                2: [(0, -1)],
                3: [(-1, 0)]
            }  
            for i in range(4):
                if check[i] == False:
                    xNum, yNum = moves[i][0]
                    coordX = x + xNum
                    coordY = y + yNum
                    if 0 <= coordX < 16 and 0 <= coordY < 16 and isVisitedMaze[coordY][coordX]:
                        queue.append((coordX, coordY))
                        answ = findSmallestDistance(x, y, wallsMaze, isVisitedMaze, returnMaze) + 1
                        if answ < returnMaze[y][x]:
                            returnMaze[y][x] = answ
    return returnMaze
    

def move(x, y, orient, maze, goal, isVisitedMaze, distanceMaze, junctionQueue, wallsMaze, state):
    L = API.wallLeft()
    R = API.wallRight()
    F = API.wallFront()
    updateWalls(x, y, orient, L, R, F, wallsMaze)
    decisionQueue = []
    
    moves = {
        0: [[(-1, 0),'Left'], [(0, 1),'Forward'], [(1, 0),'Right']],  
        1: [[(0, 1),'Left'], [(1, 0),'Forward'], [(0, -1),'Right']],  
        2: [[(1, 0),'Left'], [(0, -1),'Forward'], [(-1, 0),'Right']], 
        3: [[(0, -1),'Left'], [(-1, 0),'Forward'], [(0, 1),'Right']]  
    }
    
    for i in range(3):
        xNum, yNum = moves[orient][i][0]
        coordX = x + xNum
        coordY = y + yNum
        if not [L, F, R][i]:
            if 0 <= coordX < 16 and 0 <= coordY < 16 and checkCell(coordX, coordY, cells) == 1:
                decisionQueue.append([(coordX, coordY), isVisitedMaze[coordY][coordX], moves[orient][i][1], distanceMaze[coordY][coordX]])
            
            
    if len(decisionQueue) == 0:
        return 'RR'
    else:
        if state == 2:
            visited_moves = [move for move in decisionQueue if move[1] >= 1]
            if visited_moves:
                next_move = sorted(visited_moves, key=lambda x: x[3])[0]
                
                print(f"Next move is {next_move}", (L, F, R))
        else:
            next_move = sorted(decisionQueue, key=lambda x: (x[1],x[2]))[0]
        
        if len(decisionQueue) > 1 and (x,y) not in [(7,7), (8,7), (7,8), (8,8)] and state != 1:
            print(f"Junction at ({x}, {y})")
            junctionQueue.append([(x,y),next_move[0]])
            
        coordX, coordY = next_move[0]
        direction = next_move[2]
        
        return direction

def main():
    x, y = 0, 0
    orient = 0  
    goal = (7, 8)
    crackX, crackY = -1, -1 
    isVisitedMaze = [[0 for _ in range(16)] for _ in range(16)]
    runVisitedMaze = [[0 for _ in range(16)] for _ in range(16)]
    isVisitedMaze[0][0] += 1 
    junctionQueue = []
    junctionMaze = []
    answer = []
    state = 0
    wallsMaze = create_maze(16, 16)
    returnMaze = [[1000 for _ in range(16)] for _ in range(16)]
    runMaze = [[1000 for _ in range(16)] for _ in range(16)]
    returnMaze[0][0] = 0
    
    while True:
        if state != 2:
            returnMaze = floodfill(x, y, isVisitedMaze, returnMaze, wallsMaze)
        else:
            runMaze = floodfill(x, y, runVisitedMaze, runMaze, wallsMaze, 3)
        print(state)
        print(f"Current position: ({x}, {y}), Orientation: {orient}, beabadoobee")
    
        API.setColor(8, 8, 'G')
        API.setColor(8, 7, 'G')
        API.setColor(7, 8, 'G')
        API.setColor(7, 7, 'G')  
        API.setColor(x, y, 'R')
        
        if ((x, y) in [(7, 7), (8, 7), (7, 8), (8, 8)]) and state != 2 and state != 3:
                print(f"position is {x}, {y}")
                arr = [(7, 7), (8, 7), (7, 8), (8, 8)]
                arr.remove((x, y)) 
                for i in arr:
                    cells[i[1]][i[0]] = 1000
                    runMaze[i[1]][i[0]] = 1000
                    print(f"Ban coordinates ({i[0]}, {i[1]}) and  position is {x}, {y}")
                state = 2
                runMaze[y][x] = 0
                goal = (x, y)
                print(returnMaze)
        
        
        if True:
            if state == 3:
                print(goal)
                if (x,y) == goal:
                    return 'GOAL REACHED'
                direction = move(x, y, orient, cells, goal, isVisitedMaze, runMaze, junctionQueue, wallsMaze, 2)
                answer.append((x,y))
            elif state == 2:
                if (x,y) == (0,0):
                    state = 3
                direction = move(x, y, orient, cells, goal, isVisitedMaze, returnMaze, junctionQueue, wallsMaze, 2)
            elif state == 0:
                direction = move(x, y, orient, cells, goal, isVisitedMaze, flood, junctionQueue, wallsMaze, state)
            elif state == 1:
                junctionMaze = manhattan_distance(flood2, junctionQueue[-1][0])
                direction = move(x, y, orient, cells, goal, isVisitedMaze, junctionMaze, junctionQueue, wallsMaze, state)
            if direction == 'Left':
                API.turnLeft()
                orient = orientation(orient, 'L')
                API.moveForward()
                x, y = updateCoordinates(x, y, orient)
                
                if state == 1:
                    if x == junctionQueue[-1][0][0] and y == junctionQueue[-1][0][1]:
                        state = 0
                        xCoord, yCoord = junctionQueue[-1][1]
                        cells[yCoord][xCoord] = 1000
                        junctionQueue = []
                        print(f"Ban coordinates ({xCoord}, {yCoord})")
                    else:
                        isVisitedMaze[y][x] = 0
                        cells[y][x] = 1000
            elif direction == 'Right':
                API.turnRight()
                orient = orientation(orient, 'R')
                API.moveForward()
                x, y = updateCoordinates(x, y, orient)
                
                if state == 1:
                    if x == junctionQueue[-1][0][0] and y == junctionQueue[-1][0][1]:
                        state = 0
                        xCoord, yCoord = junctionQueue[-1][1]
                        cells[yCoord][xCoord] = 1000
                        junctionQueue = []
                        print(f"Ban coordinates ({xCoord}, {yCoord})")
                    else:
                        isVisitedMaze[y][x] = 0
                        cells[y][x] = 1000
            elif direction == 'RR':
                API.turnRight()
                API.turnRight()
                orient = orientation(orient, 'B')
                if state == 2 or state == 3:
                    pass
                else:
                    if (x,y) == (0,0):
                        pass
                    else: 
                        state = 1
            elif direction == 'Forward':
                API.moveForward()
                x, y = updateCoordinates(x, y, orient)
                
                if state == 1:
                    if x == junctionQueue[-1][0][0] and y == junctionQueue[-1][0][1]:
                        state = 0
                        xCoord, yCoord = junctionQueue[-1][1]
                        cells[yCoord][xCoord] = 1000
                        junctionQueue = []
                        print(f"Ban coordinates ({xCoord}, {yCoord})")
                    else:
                        isVisitedMaze[y][x] = 0
                        cells[y][x] = 1000
        
        if state == 2 or state == 3:
            runVisitedMaze[y][x] += 1
        isVisitedMaze[y][x] += 1 
    return "Goal Reached"

if __name__ == "__main__":
    main()