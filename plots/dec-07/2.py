import csv
import io
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

lines = []

nos = {'query_3': 0, 'query_4': 1, 'query_6': 2, 'query_7': 3, 'query_9': 4, 'query_11': 5, 'query_23': 6}
nos1 = {'query_3': [], 'query_4': [], 'query_6': [], 'query_7': [], 'query_9': [], 'query_11': [], 'query_23': []}
query_comp = {}
comp = {}

with io.open("C:\Users\Beast\Documents\IISc\Research\plots\dec-01\\100k_a_700_cm.csv", "r", encoding='utf-8-sig') as f:
    for line in f:
        l = line[:-1].split(",")
        query_no = l[0]
        query_type = l[1]
        split = l[2]
        ss = l[3]
        if split=='0' and ss=='0':
            nos1[query_type].append(l[11])

for i in range(100):
    a = [0 for k in range(7)]
    for j in nos1:
        a[nos[j]] = nos1[j][i]
    lines.append(a)

with open('100k_a_result.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)
