import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Test_Data.txt')

df.plot.scatter(x='Time',y='Do')
plt.grid()
plt.show()

