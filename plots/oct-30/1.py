import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

lines = []

nos = {'query_3': 4, 'query_4': 3, 'query_5': 3, 'query_6': 4, 'query_7': 5}
query_comp = {}
comp = {}

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-30\\10kdw_path.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        print len(l), l
        if len(l) == 6:
            query_no = l[1].split(':')[-1]
            query_type = l[2].split(":")[1]
            time = l[4].split(":")[1]
            result = l[5].split(":")[1]
            lines.append([query_no, query_type, time, 0, 0, 0, 0, 0, result, 0, 0])
        elif len(l) == 7:
            if l[-3] == 'Superstep:-1':
                query_no = l[1].split(':')[-1]
                query_type = l[2].split(":")[1]
                global_ss = int(l[3].split(":")[1])
                query_comp[query_no] = []
                for j in range(nos[query_type]):
                    query_comp[query_no].append(0)
                    comp[global_ss+j] = (query_no, j)

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-30\\10kdw_path_comp.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(" ")
        t = float(l[11]) * 1000
        ss = int(l[18][:-1])
        if ss in comp:
            query_comp[comp[ss][0]][comp[ss][1]] = max(query_comp[comp[ss][0]][comp[ss][1]], t)


for i in range(len(lines)):
    query_no = lines[i][0]
    s = 0
    for j in query_comp[query_no]:
        s += j
    lines[i][3] = s

query_comp = {}
comp = {}


with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-30\\10kdw_tree_only.log") as f:
    skip = 0
    old = 0
    i = 0
    for line in f:
        l = line[:-1].split(",")
        # print len(l), l
        if len(l) == 6:
            query_no = l[1].split(':')[-1]
            query_type = l[2].split(":")[1]
            time = l[4].split(":")[1]
            result = l[5].split(":")[1]
            lines[i][4] = time
            lines[i][-2] = result
            i += 1
        elif len(l) == 7:
            if l[-3] == 'Superstep:-1':
                query_no = l[1].split(':')[-1]
                query_type = l[2].split(":")[1]
                global_ss = int(l[3].split(":")[1])
                query_comp[query_no] = []
                for j in range(nos[query_type]):
                    query_comp[query_no].append(0)
                    comp[global_ss+j] = (query_no, j)

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-30\\10kdw_tree_only_comp.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(" ")
        t = float(l[11]) * 1000
        ss = int(l[18][:-1])
        if ss in comp:
            query_comp[comp[ss][0]][comp[ss][1]] = max(query_comp[comp[ss][0]][comp[ss][1]], t)

for i in range(len(lines)):
    query_no = lines[i][0]
    s = 0
    for j in query_comp[query_no]:
        s += j
    lines[i][5] = s


query_comp = {}
comp = {}


with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-29\\10k_f_parti4.log") as f:
    skip = 0
    old = 0
    i = 0
    for line in f:
        l = line[:-1].split(",")
        # print len(l), l
        if len(l) == 6:
            query_no = l[1].split(':')[-1]
            query_type = l[2].split(":")[1]
            time = l[4].split(":")[1]
            result = l[5].split(":")[1]
            lines[i][6] = time
            lines[i][-1] = result
            i += 1
        elif len(l) == 7:
            if l[-3] == 'Superstep:-1':
                query_no = l[1].split(':')[-1]
                query_type = l[2].split(":")[1]
                global_ss = int(l[3].split(":")[1])
                query_comp[query_no] = []
                for j in range(nos[query_type]):
                    query_comp[query_no].append(0)
                    comp[global_ss+j] = (query_no, j)

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-29\\10k_f_parti4_comp.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(" ")
        t = float(l[11]) * 1000
        ss = int(l[18][:-1])
        if ss in comp:
            query_comp[comp[ss][0]][comp[ss][1]] = max(query_comp[comp[ss][0]][comp[ss][1]], t)

for i in range(len(lines)):
    query_no = lines[i][0]
    s = 0
    for j in query_comp[query_no]:
        s += j
    lines[i][7] = s


#
#
# for i in temp:
#     lines.append(temp[i])
#
with open('10k_dw.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)