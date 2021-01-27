import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas

data = np.random.rand(10,7)
cov = np.cov(data.T) #Cov compute the 0-d features --> cov.shape = (7,7)
Cov = pandas.DataFrame(cov,columns = range(np.shape(cov)[1]))
fig = plt.figure(figsize=(15,6))
ax1 = plt.subplot(121)
sns.violinplot(data=cov,palette="Set3",linewidth=1)

ax2 = plt.subplot(122)
sns.heatmap(Cov,annot = False,linewidths=.5)
ax2.set_xlabel("XXXXX")
ax1.set_ylabel("YYYYY")
plt.show()
'''
# Load the example flights dataset and conver to long-form
flights_long = sns.load_dataset("flights")
flights = flights_long.pivot("month", "year", "passengers")

# Draw a heatmap with the numeric values in each cell
f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(flights, annot=True, fmt="d", linewidths=.5, ax=ax)
'''
