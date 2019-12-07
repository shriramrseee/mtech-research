import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}
repeat = {'query_3': 3, 'query_4': 2, 'query_5': 2, 'query_6': 3,'query_7': 4}
lines = []

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-21\\10k_f_cost_exp_2.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(":::")
        print l, len(l)
        if len(l) == 2:
            type = l[0].split(",")[-2].split(":")[1]
            for i in range(0, repeat[type]):
                lines.append([l[1]])

with open('10k_F_ind_cost_exp_queries.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)