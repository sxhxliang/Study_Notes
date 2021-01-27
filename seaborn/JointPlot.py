import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([1,5,5,8,5,4,3,2,1])
y = np.array([1,2,3,4,5,4,3,2,1])
#sns.kdeplot(x,y,cmap='Purples_d',shade=True,cbar=True)
JG1 = sns.jointplot(x,y,cmap = 'summer',kind='hex',size=5)
JG2 = sns.jointplot(x,y,cmap = 'summer',kind = 'kde',size = 5)

#subplots migration
f = plt.figure()
for J in [JG1, JG2]:
    for A in J.fig.axes:
        f._axstack.add(f._make_key(A), A)

#subplots size adjustment
f.axes[0].set_position([0.05, 0.05, 0.4,  0.4])
f.axes[1].set_position([0.05, 0.45, 0.4,  0.05])
f.axes[2].set_position([0.45, 0.05, 0.05, 0.4])
f.axes[3].set_position([0.55, 0.05, 0.4,  0.4])
f.axes[4].set_position([0.55, 0.45, 0.4,  0.05])
f.axes[5].set_position([0.95, 0.05, 0.05, 0.4])
plt.show()
