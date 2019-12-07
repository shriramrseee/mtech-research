import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

lines = []

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-28\\10k_f_path1.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        print len(l), l
        if len(l) == 5:
            query_no = l[1].split(':')[-1]
            query_type = l[2].split(":")[1]
            time = l[3].split(":")[1]
            result = l[4].split(":")[1]
            lines.append([query_no, query_type, time, 0, result, 0])

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-28\\10k_f_tree2.log") as f:
    skip = 0
    old = 0
    i = 0
    for line in f:
        l = line[:-1].split(",")
        print len(l), l
        if len(l) == 5:
            query_no = l[1].split(':')[-1]
            query_type = l[2].split(":")[1]
            time = l[3].split(":")[1]
            result = l[4].split(":")[1]
            lines[i][3] = time
            lines[i][5] = result
            i += 1


#
#
# for i in temp:
#     lines.append(temp[i])
#
with open('10k_f_1.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)