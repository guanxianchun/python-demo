import  matplotlib.pyplot as plt
import numpy as np
dict = {'A': 40, 'B': 70, 'C': 30, 'D': 85}
for i, key in enumerate(dict):#Circulate both index and value(Here is key)
    plt.bar(i, dict[key], color='r', width=0.2)
plt.xticks(np.arange(len(dict))+0.1, dict.keys())#Translation
plt.yticks(dict.values())
plt.grid(True)
plt.show()