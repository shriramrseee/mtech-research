import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

lines = []

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-24\\10k_F_1.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        print len(l), l
        if len(l) == 8:
            query_no = l[1].split(':')[-1]
            query_side = "Left"
            query_split = l[2].split(":")[1]
            query_type = l[3].split(":")[1]
            key = query_no + '-' + query_side + '-' + query_split + '-' + query_type
            if l[-4].split(':')[0] == 'iv':
                iv = l[4].split(":")[1]
                av = l[5].split(":")[1]
                te = l[6].split(":")[1]
                ae = l[7].split(":")[1]
                temp[key] = [query_no, query_side, query_split, query_type, iv, av, 0, te, 0, ae, 0]
            else:
                av = l[6].split(":")[1]
                te = l[7].split(":")[1]
                ae = l[8].split(":")[1]
                temp[key][-1] = ae
                temp[key][-3] = te
                temp[key][-5] = av
        elif len(l) == 6:
            query_no = l[1].split(':')[-1]
            query_side = "Left"
            query_split = l[2].split(":")[1]
            query_type = l[3].split(":")[1]
            key = query_no + '-' + query_side + '-' + query_split + '-' + query_type
            iv = 0
            av = 0
            te = 0
            ae = 9152392
            temp[key] = [query_no, query_side, query_split, query_type, iv, av, 0, te, 0, ae, 0]


for i in temp:
    lines.append(temp[i])

with open('10k_F_1.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)