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

with open("C:\Users\Beast\Documents\IISc\Research\logs\\nov-06\\100kzf_all1.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        # print len(l), l
        if len(l) == 4:
            ss = l[1].split(':')[-1]
            type = l[1].split(':')[-2]
            worker = l[2]
            used = l[3]
            lines.append([ss, type, worker, used])

with open('100kzf_all1.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)