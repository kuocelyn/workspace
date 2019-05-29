
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import sklearn.datasets as datasets
from pandas import Series, DataFrame
import scipy.spatial 
from scipy.spatial import ConvexHull


#get body regression parameter

def seg_m_com(mass, height):
    path = "./regre_para.csv"
    data = pd.read_csv(path)
    regre = DataFrame(data)
    link = regre['B0'] + regre['B1'] * mass + regre['B2'] * height
    return link


#get com
def seg_com(m, l, p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    z = p2[2] - p1[2]
    ratio = l/math.sqrt(x**2 + y**2 + z**2)
    x_seg = (p1[0] + (x * ratio)) * m
    y_seg = (p1[1] + (y * ratio)) * m
    z_seg = (p1[2] + (z * ratio)) * m
    return x_seg, y_seg, z_seg

def seg_com2(m, l, p):
    x_seg = p[0] * m
    y_seg = p[1] * m
    z_seg = (p[2] - l) * m
    return x_seg, y_seg, z_seg


#cal zhongchuixian
def angle_calc(a, p):
    b = np.array(a)
    q = np.array(p)
    mod_a = math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)
    e = np.dot(b.T, b)/mod_a
    f = q.T - np.dot(e, q.T)    #mid vertical line of com tipoverline

    mod_f = math.sqrt(f[0]**2 + f[1]**2 + f[2]**2)
    cross_product = np.array([-f[1], f[0], 0])
    index = np.dot(cross_product, a)
    if index > 0:
        theta = math.acos(abs(f[2]) / mod_f)
    else:
        theta = -math.acos(abs(f[2]) / mod_f)
        #flipover angle
    
    return theta

def calc():
    link = seg_m_com(70, 1690)

    dl = []
    path = "../0306zyj/zhuyujieyqzh02.csv"
    data = pd.read_csv(path, header = None, sep = '\t')
    marker_index = data[data[0].isin(["Trajectories"])].index[0]
    data = data[marker_index + 5:]
    data_f = pd.DataFrame(data, dtype = np.float)
    dl = data_f.values


    hd = 2
    c7 = hd + 12
    strn = hd + 21
    lsho = hd + 27
    lebl = hd + 33
    lwra = hd + 39
    lfin = hd + 45
    rsho = hd + 48
    rebl = hd + 54
    rwra = hd + 60
    rfin = hd + 66
    lasi = hd + 69
    lkne = hd + 84
    lank = hd + 90
    lhee = hd + 93
    ltoe = hd + 96
    rasi = hd + 72
    rkne = hd + 102
    rank = hd + 108
    rhee = hd + 111
    rtoe = hd + 114

#    com_x = []
#    com_y = []
#    com_z = []
    tipover_angle = []

    for i in range(1, len(dl)):     #100 should be len(dl)
        hd_x = (dl[i][hd] + dl[i][hd + 3] + dl[i][hd + 6] + dl[i][hd + 9])/4
        hd_y = (dl[i][hd + 1] + dl[i][hd + 4] + dl[i][hd + 7] + dl[i][hd + 10])/4
        hd_z = (dl[i][hd + 2] + dl[i][hd + 5] + dl[i][hd + 8] + dl[i][hd + 11])/4

        hd_xyz = [hd_x, hd_y, hd_z]
        c7_xyz = [dl[i][c7], dl[i][c7 + 1], dl[i][c7 + 2]]
        strn_xyz = [dl[i][strn], dl[i][strn + 1], dl[i][strn + 2]]
        lsho_xyz = [dl[i][lsho], dl[i][lsho + 1], dl[i][lsho + 2]]
        lebl_xyz = [dl[i][lebl], dl[i][lebl + 1], dl[i][lebl + 2]]
        lwra_xyz = [dl[i][lwra], dl[i][lwra + 1], dl[i][lwra + 2]]
        lfin_xyz = [dl[i][lfin], dl[i][lfin + 1], dl[i][lfin + 2]]
        rsho_xyz = [dl[i][rsho], dl[i][rsho + 1], dl[i][rsho + 2]]
        rebl_xyz = [dl[i][rebl], dl[i][rebl + 1], dl[i][rebl + 2]]
        rwra_xyz = [dl[i][rwra], dl[i][rwra + 1], dl[i][rwra + 2]]
        rfin_xyz = [dl[i][rfin], dl[i][rfin + 1], dl[i][rfin + 2]]
        lasi_xyz = [dl[i][lasi], dl[i][lasi + 1], dl[i][lasi + 2]]
        lkne_xyz = [dl[i][lkne], dl[i][lkne + 1], dl[i][lkne + 2]]
        lank_xyz = [dl[i][lank], dl[i][lank + 1], dl[i][lank + 2]]
        lhee_xyz = [dl[i][lhee], dl[i][lhee + 1], dl[i][lhee + 2]]
        ltoe_xyz = [dl[i][ltoe], dl[i][ltoe + 1], dl[i][ltoe + 2]]
        rasi_xyz = [dl[i][rasi], dl[i][rasi + 1], dl[i][rasi + 2]]
        rkne_xyz = [dl[i][rkne], dl[i][rkne + 1], dl[i][rkne + 2]]
        rank_xyz = [dl[i][rank], dl[i][rank + 1], dl[i][rank + 2]]
        rhee_xyz = [dl[i][rhee], dl[i][rhee + 1], dl[i][rhee + 2]]
        rtoe_xyz = [dl[i][rtoe], dl[i][rtoe + 1], dl[i][rtoe + 2]]

        hd_x, hd_y, hd_z = seg_com2(link[0], link[1] - 50, hd_xyz)
        upbo_x, upbo_y, upbo_z = seg_com(link[2], link[3], c7_xyz, strn_xyz)
        lobo_x, lobo_y, lobo_z = seg_com2(link[4], link[5], strn_xyz)
        lth_x, lth_y, lth_z = seg_com(link[6], link[7], lkne_xyz, lasi_xyz)
        lsh_x, lsh_y, lsh_z = seg_com(link[8], link[9], lank_xyz, lkne_xyz)
        lft_x, lft_y, lft_z = seg_com(link[10], link[11], lhee_xyz, ltoe_xyz)
        rth_x, rth_y, rth_z = seg_com(link[6], link[7], rkne_xyz, rasi_xyz)
        rsh_x, rsh_y, rsh_z = seg_com(link[8], link[9], rank_xyz, rkne_xyz)
        rft_x, rft_y, rft_z = seg_com(link[10], link[11], rhee_xyz, rtoe_xyz)
        lua_x, lua_y, lua_z = seg_com(link[12], link[13], lebl_xyz, lsho_xyz)
        lfa_x, lfa_y, lfa_z = seg_com(link[14], link[15], lwra_xyz, lebl_xyz)
        lhd_x, lhd_y, lhd_z = seg_com2(link[16], 0, lfin_xyz)
        rua_x, rua_y, rua_z = seg_com(link[12], link[13], rebl_xyz, rsho_xyz)
        rfa_x, rfa_y, rfa_z = seg_com(link[14], link[15], rwra_xyz, rebl_xyz)
        rhd_x, rhd_y, rhd_z = seg_com2(link[16], 0, rfin_xyz)

#        com_x.append((hd_x + upbo_x + lobo_x + lth_x + lsh_x + lft_x + rth_x + rsh_x + rft_x + lua_x + lfa_x + lhd_x + rua_x + rfa_x + rhd_x)/70)
#        com_y.append((hd_y + upbo_y + lobo_y + lth_y + lsh_y + lft_y + rth_y + rsh_y + rft_y + lua_y + lfa_y + lhd_y + rua_y + rfa_y + rhd_y)/70)
#        com_z.append((hd_z + upbo_z + lobo_z + lth_z + lsh_z + lft_z + rth_z + rsh_z + rft_z + lua_z + lfa_z + lhd_z + rua_z + rfa_z + rhd_z)/70)
        
        com_x = (hd_x + upbo_x + lobo_x + lth_x + lsh_x + lft_x + rth_x + rsh_x + rft_x + lua_x + lfa_x + lhd_x + rua_x + rfa_x + rhd_x)/70
        com_y = (hd_y + upbo_y + lobo_y + lth_y + lsh_y + lft_y + rth_y + rsh_y + rft_y + lua_y + lfa_y + lhd_y + rua_y + rfa_y + rhd_y)/70
        com_z = (hd_z + upbo_z + lobo_z + lth_z + lsh_z + lft_z + rth_z + rsh_z + rft_z + lua_z + lfa_z + lhd_z + rua_z + rfa_z + rhd_z)/70
#        com = [com_x, com_y, com_z]

#        plt.xlabel = 'com_x'
#        plt.ylabel = 'com_y'
#        plt.scatter(com_x, com_y, marker='x', color='r', s=10)

#bos
        points = [ltoe_xyz[0:2], lank_xyz[0:2], lhee_xyz[0:2], rhee_xyz[0:2], rank_xyz[0:2], rtoe_xyz[0:2]]
#        for point in points:
#            plt.scatter(point[0], point[1], marker='o', c='y')
            
        cv = ConvexHull(points)
        hull = cv.vertices.tolist()
        print(hull)
        #convinient to draw BOS
        result = []
        for j in range(0, len(hull)):
            result.append(points[hull[j]])
        result.append(points[hull[0]])
        
#        for i in range(0, len(result) - 1):
#            plt.plot([result[i][0], result[i+1][0]], [result[i][1], result[i+1][1]], c = 'r')
#        plt.show()

#stable pyramid
        tipover_line = []   #all the flipover line
        tipover_point = []   #vector from com to flipover points
        tipover_angle1 = []   #angle between com vertical line and the mid vertical line of tipover line

        for j in range(0, len(result)-1):
            tipover_line.append([result[j][0] - result[j+1][0], result[j][1] - result[j+1][1], 0])
            tipover_point.append([result[j][0]-com_x, result[j][1]-com_y, -com_z])
            tipover_angle1.append(angle_calc(tipover_line[j], tipover_point[j]))
        tipover_angle.append(tipover_angle1)   
#       print(tipover_angle)
        
#    for i in range(0, len(dl)-1):
#        plt.scatter(i, tipover_angle[i][4], marker='o', color='g', s=10)
#    plt.show()

            
        

if __name__ == "__main__":
    calc()










