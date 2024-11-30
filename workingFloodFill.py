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

def updateWalls(x,y,orient,L,R,F):
    if(L and R and F):
        if (orient==0): 
            cells[y][x]= 13
        elif (orient==1): 
            cells[y][x]= 12
        elif (orient==2): 
            cells[y][x]= 11
        elif (orient==3): 
            cells[y][x]= 14

    elif (L and R and not F):
        if (orient==0 or orient== 2): 
            cells[y][x]= 9
        elif (orient==1 or orient==3): 
            cells[y][x]= 10

    elif (L and F and not R):
        if (orient==0): 
            cells[y][x]= 8
        elif (orient==1): 
            cells[y][x]= 7
        elif (orient==2): 
            cells[y][x]= 6
        elif (orient==3): 
            cells[y][x]= 5

    elif (R and F and not L):
        if (orient==0): 
            cells[y][x]= 7
        elif (orient==1): 
            cells[y][x]= 6
        elif (orient==2): 
            cells[y][x]= 5
        elif (orient==3): 
            cells[y][x]= 8

    elif(F):
        if (orient==0): 
            cells[y][x]= 2
        elif (orient==1): 
            cells[y][x]= 3
        elif (orient==2): 
            cells[y][x]= 4
        elif (orient==3): 
            cells[y][x]= 1

    elif(L):
        if (orient==0): 
            cells[y][x]= 1
        elif (orient==1): 
            cells[y][x]= 2
        elif (orient==2): 
            cells[y][x]= 3
        elif (orient==3): 
            cells[y][x]= 4

    elif(R):
        if (orient==0): 
            cells[y][x]= 3
        elif (orient==1): 
            cells[y][x]= 4
        elif (orient==2): 
            cells[y][x]= 1
        elif (orient==3): 
            cells[y][x]= 2

    else:
        cells[y][x]= 15

def create_maze(width: int = 5, height: int = 5):
    return [[[False, False, False, False] for _ in range(width)] for _ in range(height)]

def add_horizontal_wall(maze, x_coordinate, horizontal_line):
    if 0 <= horizontal_line < len(maze) and 0 <= x_coordinate < len(maze[0]):
        maze[horizontal_line][x_coordinate][2] = True
    if 0 <= horizontal_line - 1 < len(maze) and 0 <= x_coordinate < len(maze[0]):
        maze[horizontal_line-1][x_coordinate][0] = True
    return maze

def add_vertical_wall(maze, y_coordinate, vertical_line):
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line < len(maze[0]):
        maze[y_coordinate][vertical_line][1] = True
    if 0 <= y_coordinate < len(maze) and 0 <= vertical_line - 1 < len(maze[0]):
        maze[y_coordinate][vertical_line-1][3] = True
    return maze

def get_dimensions(maze) -> Tuple[int, int]:
    return len(maze[0]), len(maze)

def get_walls(maze, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    return maze[y_coordinate][x_coordinate]

def sense_walls(maze, x,y) -> tuple[bool, bool, bool,bool]:
    return tuple(get_walls(maze, x,y))

def findSmallestDistance(x, y, wallsMaze, isVisitedMaze):
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
            
def floodfill(startX, startY, isVisitedMaze, returnMaze, wallsMaze):
    queue = [(startX, startY)]
    while True:
        x, y = queue.pop(0)
        if len(queue) == 0:
            return returnMaze
        check = sense_walls(wallsMaze, startX, startY)
        moves = {
            0: [(0, 1)],  
            1: [(1, 0)],
            2: [(0, -1)],
            3: [(-1, 0)]
        }  
        for i in range(4):
            if check[i] == False:
                xNum, yNum = moves[i][0]
                coordX = startX + xNum
                coordY = startY + yNum
                if 0 <= coordX < 16 and 0 <= coordY < 16 and isVisitedMaze[coordY][coordX] and cells[coordY][coordX] == 0:
                    queue.append((coordX, coordY))
                    returnMaze[coordY][coordX] = findSmallestDistance(coordX, coordY, wallsMaze, isVisitedMaze) + 1

def move(x, y, orient, maze, goal, isVisitedMaze, distanceMaze, junctionQueue, wallsMaze, state):
    L = API.wallLeft()
    R = API.wallRight()
    F = API.wallFront()
    updateWalls(x, y, orient, L, R, F)
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
        else:
            print(f"Wall at ({coordX}, {coordY})")
            if orient == 0:
                add_horizontal_wall(wallsMaze, coordX, coordY)
            elif orient == 1:
                add_vertical_wall(wallsMaze, x, y)
            elif orient == 2:
                add_horizontal_wall(wallsMaze, x, y)
            elif orient == 3:
                add_vertical_wall(wallsMaze, coordY, coordX)
    if len(decisionQueue) == 0:
        return 'RR'
    else:
        if state == 3:
            visited_moves = [move for move in decisionQueue if move[1] >= 1]
            if visited_moves:
                next_move = sorted(visited_moves, key=lambda x: x[3])[0]
        elif any([x[3] < 5 for x in decisionQueue]):
            if(any([x[1] > 2 for x in decisionQueue])):
                next_move = sorted(decisionQueue, key=lambda x: (x[1],x[3]))[0]
            else:
                next_move = sorted(decisionQueue, key=lambda x: (x[3],x[1]))[0]
        else:
            next_move = sorted(decisionQueue, key=lambda x: (x[1],x[3]))[0]
        
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
    isVisitedMaze[0][0] += 1 
    junctionQueue = []
    junctionMaze = []
    answer = []
    state = 0
    wallsMaze = create_maze(16, 16)
    returnMaze = [[1000 for _ in range(16)] for _ in range(16)]
    
    while True:
        print(state)
        
        if state == 3:
            if (x,y) == (0,0):
                return answer
            returnMaze = floodfill(crackX, crackY, isVisitedMaze, returnMaze, wallsMaze)
            direction = move(x, y, orient, cells, goal, isVisitedMaze, returnMaze, junctionQueue, wallsMaze, 3)
            answer.append((x,y))
        API.setColor(x, y, 'R')
        API.setColor(8, 8, 'G')
        API.setColor(8, 7, 'G')
        API.setColor(7, 8, 'G')
        API.setColor(7, 7, 'G')  
        print(f"Current position: ({x}, {y}), Orientation: {orient}")
        if state == 0:
            direction = move(x, y, orient, cells, goal, isVisitedMaze, flood, junctionQueue, wallsMaze, state)
        else:
            junctionMaze = manhattan_distance(flood2, junctionQueue[-1][0])
            direction = move(x, y, orient, cells, goal, isVisitedMaze, junctionMaze, junctionQueue, wallsMaze, state)
            
            
        if (x, y) in [(7, 7), (8, 7), (7, 8), (8, 8)] and state != 3:
                print(f"position is {x}, {y}")
                returnMaze[y][x] = 0
                crackX, crackY = (x, y)
                print(returnMaze)
                arr = [(7, 7), (8, 7), (7, 8), (8, 8)]
                arr.remove((x, y)) 
                for i in arr:
                    cells[i[1]][i[0]] = 1000
                    print(f"Ban coordinates ({i[0]}, {i[1]}) and  position is {x}, {y}")
                state = 3
        else:
            if direction == 'Left':
                API.turnLeft()
                orient = orientation(orient, 'L')
                API.moveForward()
                x, y = updateCoordinates(x, y, orient)
                
                if state == 1 and x == junctionQueue[-1][0][0] and y == junctionQueue[-1][0][1]:
                    state = 0
                    xCoord, yCoord = junctionQueue[-1][1]
                    junctionQueue = []
                    cells[yCoord][xCoord] = 1000
                    print(f"Ban coordinates ({xCoord}, {yCoord})")
            elif direction == 'Right':
                API.turnRight()
                orient = orientation(orient, 'R')
                API.moveForward()
                x, y = updateCoordinates(x, y, orient)
                
                if state == 1 and x == junctionQueue[-1][0][0] and y == junctionQueue[-1][0][1]:
                    state = 0
                    xCoord, yCoord = junctionQueue[-1][1]
                    junctionQueue = []
                    cells[yCoord][xCoord] = 1000
                    print(f"Ban coordinates ({xCoord}, {yCoord})")
            elif direction == 'RR':
                API.turnRight()
                API.turnRight()
                orient = orientation(orient, 'B')
                if state == 3:
                    pass
                else:
                    state = 1
            elif direction == 'Forward':
                API.moveForward()
                x, y = updateCoordinates(x, y, orient)
                
                if state == 1 and x == junctionQueue[-1][0][0] and y == junctionQueue[-1][0][1]:
                    state = 0
                    xCoord, yCoord = junctionQueue[-1][1]
                    junctionQueue = []
                    cells[yCoord][xCoord] = 1000
                    print(f"Ban coordinates ({xCoord}, {yCoord})")

        
        isVisitedMaze[y][x] += 1 
    return "Goal Reached"

if __name__ == "__main__":
    main()