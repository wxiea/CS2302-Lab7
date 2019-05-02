import matplotlib.pyplot as plt
import numpy as np
import random
import time
import dsf
import adj
import queue

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

# This loop created in case user wants to remove more walls than the ones in the maze
while True:
    NumberRemove = int(input('How many walls do you want to remove: '))  # Asks user for number of walls to be removed
    # This checks if the user wants to remove more walls than there are in the maze.
    if NumberRemove > len(walls)-1:
        print('The number of walls you want to remove exeeds the number of walls that are present.')
        continue  # This will cause the loop to continue and ask the user to select less walls to remove        
    if NumberRemove > NumberWall-1:
        print('There is at least one path from source to destination (m > n-1).')
        break  # Will exit loop
    if NumberRemove < NumberWall-1:
        print('A path from source to destination is not guaranteed to exist (m < n-1).')
        break  # Will exit loop
    if NumberRemove == NumberWall-1:
        print('There is a unique path from source to destination (m = n-1).')
        break  # will exit loop

def get_adj_list(p, A):
    for i in range(len(p)):
        temp0 = p[i][0]
        temp1 = p[i][1]
        A[temp0].append(temp1)
        A[temp1].append(temp0)
    return A

"""
def Union_Maze(maze, wall, move):  # creates a maze and asks the user how many walls to remove  
    g = adj.Graph()
    for i in range(NumberWall):
        g.addVertex(i)
    while move > 0:
        d = random.randint(0, len(walls)-1) # d equals the wall to be removed at random       
        if dsf.union_c(maze, walls[d][0], walls[d][1]):
            walls.pop(d)
            g.addEdge(walls[d][0], walls[d][1])
            move -= 1
    for v in g:
        for w in v.getConnections():
            print("( %s , %s )" % (v.getId(), w.getId()))
    return g 
"""

def Union_Maze(maze, wall, move):  # creates a maze and asks the user how many walls to remove  
    g = []
    temp = [[] for i in range(NumberWall)]
    while move > 0:
        d = random.randint(0, len(walls)-1) # d equals the wall to be removed at random       
        if dsf.union(maze, walls[d][0], walls[d][1]):
            g.append(walls.pop(d))
            move -= 1
    
    for i in range(len(g)):
        temp0 = g[i][0]
        temp1 = g[i][1]
        temp[temp0].append(temp1)
        temp[temp1].append(temp0)
    return temp 

G = Union_Maze(maze, walls, NumberRemove)


def breadth_first_search(G):
    visited = [False] * NumberWall 
    prev = [-1] * NumberWall
    Q = adj.Graph()
    Q.addVertex(0)
    visited[0] = True 
    for i in Q:
        v = Q.getVertex(i).item
        for t in G[v]:
            if not visited[t]:
                visited[t] = True
                prev[t] = v
                Q.addVertex(t)
    return prev
    
#bfs = breadth_first_search(G)

def depth_first_search_recursion(G, source):
    visited = [False] * NumberWall
    prev = [-1] * NumberWall
    visited[source] = True
    for t in G[source]:
        if not visited[t]:
            prev[t] = source 
    return prev
dfs = depth_first_search_recursion(G,0)


def path(plot, previous, vertex, x, y) :
    if previous[vertex] != -1: 
        if vertex == (previous[vertex] + maze_cols) :
            x1 = x
            y1 = y - 1
            path(plot, previous, previous[vertex], x1, y1)
            plot.plot([x1, x], [y1, y], linewidth = 2, color = 'r')
        if  vertex == (previous[vertex] - maze_cols) :
            x1 = x
            y1 = y + 1
            path(plot, previous, previous[vertex], x1, y1)
            plot.plot([x1, x], [y1, y], linewidth = 2, color = 'r')       
        if vertex == (previous[vertex] + 1) :
            x1 = x - 1
            y1 = y
            path(plot, previous, previous[vertex], x1, y1)
            plot.plot([x1, x], [y1, y], linewidth = 2, color = 'r')         
        if vertex == (previous[vertex] - 1) :
            x1 = x + 1
            y1 = y
            path(plot, previous, previous[vertex], x1, y1)
            plot.plot([x1, x],[y1, y], linewidth = 2, color = 'r')

def valid(maze,x,y):
    if (x>=0 and x<maze_rows and y>=0 and y<maze_cols and maze[x][y]==1):
        return True
    else:
        return False
# 移步函数实现
def walk(maze,x,y):
    # 如果位置是迷宫的出口，说明成功走出迷宫
    if(x==0 and y==0):
        print("successful!")
        return True
    # 递归主体实现
    if valid(maze,x,y):
        # print(x,y)
        maze[x][y]=2  # 做标记，防止折回
        # 针对四个方向依次试探，如果失败，撤销一步
        if not walk(maze,x-1,y):
            maze[x][y]=1
        elif not walk(maze,x,y-1):
            maze[x][y]=1
        elif not walk(maze,x+1,y):
            maze[x][y]=1
        elif not walk(maze,x,y+1):
            maze[x][y]=1
        else:
            return False  # 无路可走说明，没有解 
    return True

print(walk(dfs,0,149))       
#newmaze = draw_maze(walls,maze_rows,maze_cols)
#path(newmaze,bfs,NumberWall-1,maze_cols,maze_rows)
#draw_maze(walls,maze_rows,maze_cols)


