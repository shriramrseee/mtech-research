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

with open("C:\Users\Beast\Documents\IISc\Research\logs\\nov-12\\10kdw_neo4j.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        print len(l), l
        if len(l) == 4:
            query_no = l[0].split(" ")[-1]
            query_type = l[1].split(":")[-1]
            query_start = long(l[-1].split("::")[-1])
            query_comp[query_no] = [query_no, query_type, query_start, 0, 0]
        elif len(l) == 6:
            query_no = l[0].split(" ")[-1]
            query_type = l[1].split(":")[-1]
            result = l[2].split(":")[-1]
            query_end = long(l[-1].split("::")[-1])
            query_comp[query_no][3] = query_end - query_comp[query_no][2]
            query_comp[query_no][4] = result


for i in query_comp:
    lines.append(query_comp[i])

with open('10kdw_neo4j.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)