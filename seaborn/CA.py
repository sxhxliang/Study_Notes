import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import axes
from matplotlib import animation
import sys

def draw_heatmap(data,Axes):
    Axes.imshow(data,interpolation = 'nearest',cmap = 'rainbow')
    
'''
fig,ax = plt.subplots()
data = np.random.rand(10,10).round()
draw_heatmap(data,ax)
plt.show()
'''

Len = 100
Init_cell = (np.random.rand(10,2)*50).round().astype(int)
Patch = (-np.array(range(Len**2))/Len**2).reshape(Len,Len)
Map = np.zeros((Len,Len))
for p in Init_cell:
    Map[p[0]:p[0]+6,p[1]:p[1]+5] = 1
dirx = [1,1,1,0,0,-1,-1,-1]
diry = [-1,0,1,-1,1,-1,0,1]

def count_neighbors(Map, x, y):
    cnt = 0
    for i in range(8):
        nx = (x + dirx[i]) % Len
        ny = (y + diry[i]) % Len
        cnt += Map[nx][ny]
    return cnt

def update_Map():
    global Map
    New_Map = Map
    for i in range(Len):
        for j in range(Len):
            num_nb = count_neighbors(Map,i,j)
            if num_nb > 4:
                New_Map[i][j] = 0
            elif num_nb == 3:
                New_Map[i][j] = 1
            elif num_nb != 2:
                New_Map[i][j] = 0 
    Map = New_Map

def Run(i):
#    if i == 9:
#        plt.close()
    draw_heatmap(Map+Patch,ax)
    update_Map()
    return ax
    

fig,ax = plt.subplots()
minor_ticks = np.arange(0,Len,1)-0.5
ax.set_xticks(minor_ticks,minor = True)
ax.set_yticks(minor_ticks,minor = True)
ax.grid(which = 'minor',linestyle = '-')

if __name__ == '__main__':
    Ani = animation.FuncAnimation(fig,Run,frames=200,interval = 1)
    #plt.show()
    Writer  = animation.writers['ffmpeg']
    writer = Writer(fps=20,bitrate=1080)
    Ani.save('line.mp4',writer=writer)










