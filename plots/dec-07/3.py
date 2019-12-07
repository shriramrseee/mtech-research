import csv
import io
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

lines = []

nos = {'query_3': 4, 'query_4': 3, 'query_6': 4, 'query_7': 5, 'query_9': 6, 'query_11': 6, 'query_23': 5}

for i in nos:
    lines = []
    with io.open("C:\Users\Beast\Documents\IISc\Research\plots\dec-07\\100k_a_"+i+".csv", "r", encoding='utf-8-sig') as f:
        for line in f:
            l = line[:-1].split(",")
            opt = float(l[-1])
            a = [100.0*(float(j)-opt)/opt for j in l[0:nos[i]]]
            lines.append(a)
    with open('100k_a_per_opt_'+i+'.csv', 'wb') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
