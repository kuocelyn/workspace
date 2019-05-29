import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = "humancrutch2/zhuyujiebingjiao01.csv"

data = pd.read_csv(path, header = None, sep = '\t')
marker_index1 = data[data[0].isin(["Devices"])].index[0]
marker_index2 = data[data[0].isin(["Model Outputs"])].index[0]
marker_index3 = data[data[0].isin(["Trajectories"])].index[0]
data1 = data[marker_index1 + 5:marker_index2 - 1]
data2 = data[marker_index2 + 5:marker_index3 - 1]
data3 = data[marker_index3 + 5:]

data_f1 = pd.DataFrame(data1, dtype = np.float)
data_f2 = pd.DataFrame(data2, dtype = np.float)
data_f3 = pd.DataFrame(data3, dtype = np.float)

data_f1.to_csv('./data/mit.csv', index=False, header=0)
data_f2.to_csv('./data/model.csv', index=False, header=0)
data_f3.to_csv('./data/marker.csv', index=False, header=0)

