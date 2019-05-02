import matplotlib.pyplot as plt
import numpy as np
import random
import time
import dsf
import adj
import queue
import matplotlib.cm as cm
from collections import deque



def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

start = time.time() 
plt.close("all") 
maze_rows = 10
maze_cols = 15

walls = wall_list(maze_rows,maze_cols)
NumberWall = maze_rows*maze_cols
maze = dsf.DisjointSetForest(maze_rows*maze_cols)
draw_maze(walls,maze_rows,maze_cols,cell_nums=True)
      
draw_maze(walls,maze_rows,maze_cols)
plt.show()

while True:
    NumberRemove = int(input('walls to remove: '))
    if NumberRemove < NumberWall-1:
        print('A path from source to destination is not guaranteed to exist ')
        break  
    if NumberRemove == NumberWall-1:
        print('The is a unique path from source to destination ')
        break
    if NumberRemove > NumberWall-1:
        print('There is at least one path from source to destination')
        break

def New_maze(maze, wall, move):  # creates a maze and asks the user how many walls to remove  
    g = []
    temp = [[] for i in range(NumberWall)]
    while move > 0:
        d = random.randint(0, len(walls)-1) # d equals the wall to be removed at random       
        if dsf.union(maze, walls[d][0], walls[d][1]):
            g.append(walls.pop(d))
            move -= 1    
    for i in range(len(g)):
        temp[g[i][0]].append(g[i][1])
        temp[g[i][1]].append(g[i][0])
    return temp 

G = New_maze(maze, walls, NumberRemove)


def find_path_bfs(image, M):
    path = np.zeros((maze_rows, maze_cols, 2))
    vis = np.zeros((maze_rows, maze_cols))
    vis[0][0] = 1
    Queue = deque()
    Queue.append((0, 0))
    while(Queue):
        temp = Queue.popleft()
        nr = temp[0]
        nc = temp[1]
 
        if (nc == maze_cols - 1) and (nr == maze_rows - 1):
            maze_rows
        if (nc > 0) and (not vis[nr][nc - 1]) and (M[nr][nc][0]):
            vis[nr][nc] = 1
            Queue.append((nr, nc - 1))
            path[nr][nc - 1][0] = nr
            path[nr][nc - 1][1] = nc
        if (nr > 0) and (not vis[nr - 1][nc]) and (M[nr][nc][1]):
            vis[nr][nc] = 1
            Queue.append((nr - 1, nc))
            path[nr - 1][nc][0] = nr
            path[nr - 1][nc][1] = nc
        if (nc < maze_cols - 1) and (not vis[nr][nc + 1]) and (M[nr][nc][2]):
            vis[nr][nc] = 1
            Queue.append((nr, nc + 1))
            path[nr][nc + 1][0] = nr
            path[nr][nc + 1][1] = nc
        if (nr < maze_rows - 1) and (not vis[nr + 1][nc]) and (M[nr][nc][3]):
            vis[nr][nc] = 1
            Queue.append((nr + 1, nc))
            path[nr + 1][nc][0] = nr
            path[nr + 1][nc][1] = nc
            
dirs=[(0,1),(1,0),(0,-1),(-1,0)] 
path=[]              
 
def mark(maze,pos):  
    maze[pos[0]][pos[1]]=2
 
def passable(maze,pos): 
    return maze[pos[0]][pos[1]]==0
 
def find_path(maze,pos,end):
    mark(maze,pos)
    if pos==end:
        print(pos,end=" ")
        path.append(pos)
        return True
    for i in range(4):
        nextp=pos[0]+dirs[i][0],pos[1]+dirs[i][1]
        if passable(maze,nextp):
            if find_path(maze,nextp,end):
                print(pos,end=" ")
                path.append(pos)
                return True
    return False
 

newmaze = draw_maze(walls,maze_rows,maze_cols)
find_path_bfs(newmaze, G)   
draw_maze(walls,maze_rows,maze_cols)


