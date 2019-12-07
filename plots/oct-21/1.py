import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

lines = []

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-21\\10k_f_cost_exp_5.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        if len(l) == 9:
            query_no = l[1].split(':')[-1]
            query_side = l[2].split(':')[1]
            query_split = l[3].split(":")[1]
            query_type = l[4].split(":")[1]
            key = query_no + '-' + query_side + '-' + query_split + '-' + query_type
            if l[-4].split(':')[0] == 'iv':
                iv = l[5].split(":")[1]
                av = l[6].split(":")[1]
                te = l[7].split(":")[1]
                ae = l[8].split(":")[1]
                temp[key] = [query_no, query_side, query_split, query_type, iv, av, 0, te, 0, ae, 0]
            else:
                av = l[6].split(":")[1]
                te = l[7].split(":")[1]
                ae = l[8].split(":")[1]
                temp[key][-1] = ae
                temp[key][-3] = te
                temp[key][-5] = av

for i in temp:
    lines.append(temp[i])

with open('10k_F_ind_cost_exp_3.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)