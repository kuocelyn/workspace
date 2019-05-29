# -*- coding: utf-8 -*-  
import string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

l_ankle_x = 92
l_ankle_y = 93
l_ankle_z = 94
l_heel_x = 95
l_heel_y = 96
l_heel_z = 97
l_toe_x = 98
l_toe_y = 99
l_toe_z = 100

r_ankle_x = 110
r_ankle_y = 111
r_ankle_z = 112
r_heel_x = 113
r_heel_y = 114
r_heel_z = 115
r_toe_x = 116
r_toe_y = 117
r_toe_z = 118

l_sen1_x_bias = 0
l_sen1_y_bias = 19.43
l_sen2_x_bias = -2.65
l_sen2_y_bias = 11.925
l_sen3_x_bias = 0
l_sen3_y_bias = 3.975

r_sen1_x_bias = 0
r_sen1_y_bias = 19.43
r_sen2_x_bias = 2.65
r_sen2_y_bias = 11.925
r_sen3_x_bias = 0
r_sen3_y_bias = 19.43

def cal_cop(l_f,r_f,l_p,r_p):
    x = (l_f*l_p[0]+r_f*r_p[0]) / (l_f+r_f)
    y = (l_f*l_p[1]+r_f*r_p[1]) / (l_f+r_f)
    return [x,y]



vicon_data_path = "../0306zyj/human/zhuyujiebingjiao02.csv"
shoepressure_data_path = "../shoepressure/03-06/bj1_19-03-06 10-40-51-293.txt"

data_list = []
data1_list = []
data = pd.read_csv(vicon_data_path, header=None,sep = '\t')
marker_index = data[data[0].isin(["Trajectories"])].index[0]
data = data[marker_index:]
data_list = data.values

#foo1 = np.array(data)
#for i in range(len(foo1)):
#    str1 = ','.join(foo1[i])
#    a = str1.split(',')
#    data_list.append(a)

vicon_index = 5
with open(shoepressure_data_path,encoding = 'utf-8') as file_to_read:
    lines = file_to_read.readlines()
    for line in lines:
        arr = line.split(',')
        if(arr[0][0].isalpha()):
            arr.append('cop')
            data1_list.append(arr)
        else:
            if(arr[4] == '********.**\n'):
                arr[4] = '0'
            elif(arr[9] == '********.**\n'):
                arr[9] = '0'
            l_f = float(arr[4])
            r_f = float(arr[9])
            l_p = [float(data_list[vicon_index][l_heel_x]), float(data_list[vicon_index][l_heel_y]) + 119.25]
            r_p = [float(data_list[vicon_index][r_heel_x]), float(data_list[vicon_index][r_heel_y]) + 119.25]
            #print(vicon_index)
            #print(l_p)
            cop = cal_cop(l_f,r_f,l_p,r_p)
            vicon_index += 1
            if(vicon_index > 2593):
                break
            arr.append(cop)
            data1_list.append(arr)
    
    vicon_index = 5
file_to_read.close()

print(data_list[1591][l_heel_x],data_list[1591][r_heel_x])
print(data1_list[1591][4],data1_list[1591][9])

x = []
y = []
for i in range(1,len(data1_list)):
    x.append(data1_list[i][10][0])
    y.append(data1_list[i][10][1])
plt.xlabel = 'x'
plt.ylabel = 'y'
plt.scatter(x,y,marker = 'x',color = 'r',s = 1)
plt.show()
    

with open('test.txt','w') as f:
    for item in data1_list:
        f.writelines(str(item))
        f.write('\n')



