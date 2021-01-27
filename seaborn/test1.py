import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig,ax = plt.subplots()
SS, = ax.plot([],[])
xdata = []
ydata = []

def generator():
    cnt = 0
    x = 0
    y = 0
    while cnt < 1000:
        cnt += 1
        x = np.random.randn(1)*100
        y = np.random.randn(1)*1000
        yield x,y

def init():
    ax.set_ylim(-1000, 1000)
    ax.set_xlim(-100, 100)
    return ax


def update(data):
    x = np.random.randn(1)*100
    y = np.random.randn(1)*1000
    xdata.append(x)
    ydata.append(y)
    ax.scatter(xdata,ydata,c = ydata)
    return ax


Ani = animation.FuncAnimation(fig,update,blit=False,repeat=False,
                              init_func=init,interval=20)
plt.show()


    
