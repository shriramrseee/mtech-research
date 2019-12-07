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

with open("C:\Users\Beast\Documents\IISc\Research\logs\\nov-23\\100k_A_500.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        if len(l) == 7:
            query_no = l[1].split(':')[-1]
            split = l[3].split(':')[-1]
            time = l[-2].split(':')[-1]
            result = l[-1].split(':')[-1]
            comp[query_no+'-'+split] = [time, result]
        elif len(l) == 14:
            query_no = l[1].split(':')[-1]
            query_type = l[2].split(":")[1]
            split = l[3].split(':')[-1]
            ss = l[5].split(':')[-1]
            iv1 = l[6].split(':')[-1]
            iv2 = l[7].split(':')[-1]
            av1 = l[8].split(':')[-1]
            av2 = l[9].split(':')[-1]
            te1 = l[10].split(':')[-1]
            te2 = l[11].split(':')[-1]
            ae1 = l[12].split(':')[-1]
            ae2 = l[13].split(':')[-1]
            if ss != '0':
                continue
            if iv1 == '0' and iv2=='0':
                continue
            if ae2 == '0':
                te2 = '0'
            if int(split) != nos[query_type]-2:
                if iv1 != '0':
                    lines.append([query_no, query_type, split, ss, 'left', iv1, av1, te1, ae1, 0, 0])
            if int(split) == nos[query_type]-2:
                if iv1 != '0':
                    lines.append([query_no, query_type, split, ss, 'right', iv1, av1, te1, ae1, 0, 0])
            if int(split) != 0 and int(split) != nos[query_type]-2:
                if iv2 != '0':
                    lines.append([query_no, query_type, split, ss, 'right', iv2, av2, te2, ae2, 0, 0])

for i in lines:
    i[-2] = comp[i[0]+'-'+i[2]][0]
    i[-1] = comp[i[0]+'-'+i[2]][1]

query_comp = {}
comp = {}

#
#
# for i in temp:
#     lines.append(temp[i])
#
with open('100k_A_500.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)