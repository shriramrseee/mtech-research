import csv
import io
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

lines = []

nos = {'query_3': 5, 'query_4': 4, 'query_6': 5, 'query_7': 6, 'query_9': 7, 'query_11': 7, 'query_23': 6}
nos1 = {'query_3': [], 'query_4': [], 'query_6': [], 'query_7': [], 'query_9': [], 'query_11': [], 'query_23': []}
nos2 = {'query_3': [], 'query_4': [], 'query_6': [], 'query_7': [], 'query_9': [], 'query_11': [], 'query_23': []}
query_comp = {}
comp = {}
comp1 = {}

with io.open("C:\Users\Beast\Documents\IISc\Research\plots\dec-07\\100k_a_700_cm.csv", "r", encoding='utf-8-sig') as f:
    for line in f:
        l = line[:-1].split(",")
        query_no = l[0]
        query_type = l[1]
        if l[6] == '1':
            if query_no not in comp:
                comp[query_no] = l[3]
            elif l[5] == '1':
                comp[query_no] = l[3]
        if l[5] == '1':
            comp1[query_no] = l[3]
        if query_no in query_comp:
            query_comp[query_no][int(l[2])+1] = l[3]
        else:
            query_comp[query_no] = [0 for i in range(nos[query_type]+1)]
            query_comp[query_no][0] = query_type
            query_comp[query_no][int(l[2])+1] = l[3]

keys = query_comp.keys()
keys.sort()
for i in keys:
    query_type = query_comp[i][0]
    query_comp[i][-1] = comp1[i]
    query_comp[i][-2] = comp[i]
    nos1[query_type].append(query_comp[i][1:])

# baseline

with io.open("C:\Users\Beast\Documents\IISc\Research\plots\dec-07\\100k_a_700_neo4j.csv", "r", encoding='utf-8-sig') as f:
    for line in f:
        l = line[:-1].split(",")
        query_no = l[0]
        query_type = 'query_'+l[1]
        if l[2] != -1:
            nos2[query_type].append([l[3], l[5]])


# for i in nos1:
#     lines = nos1[i]
#     with open('100k_a_'+i+'.csv', 'wb') as writeFile:
#         writer = csv.writer(writeFile)
#         writer.writerows(lines)

for i in nos2:
    lines = nos2[i]
    with open('100k_a_neo4j_'+i+'.csv', 'wb') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)