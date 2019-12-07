import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

lines = []

nos = {'query_3': 3, 'query_4': 2, 'query_5': 2, 'query_6': 3, 'query_7': 4, 'query_9': 5, 'query_11': 5, 'query_23': 4}
query_comp = {}
comp = {}

with open("C:\Users\Beast\Documents\IISc\Research\logs\\dec-01\\100k_f_500_cm1.log") as f:
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
        elif len(l) == 8:
            query_no = l[1].split(':')[-1]
            split = l[3].split(':')[-1]
            ss = l[5].split(':')[-1]
            msg = l[6].split(':')[-1]
            query_comp[query_no + '-' + split + '-' + ss] = [msg]
        elif len(l) == 20:
            query_no = l[1].split(':')[-1]
            query_type = l[2].split(":")[1]
            split = l[3].split(':')[-1]
            ss = l[5].split(':')[-1]
            jt1 = float(l[6].split(':')[-1])/1000000.0
            jl1 = l[7].split(':')[-1]
            jr1 = float(l[8].split(':')[-1])/1000000.0
            jlr1 = l[9].split(':')[-1]
            jc1 = float(l[10].split(':')[-1])/1000000.0
            ct1 = l[11].split(':')[-1]
            ct2 = l[12].split(':')[-1]
            cm1 = l[13].split(':')[-1]
            st1 = float(l[14].split(':')[-1])/1000000.0
            st2 = l[15].split(':')[-1]
            st3 = l[16].split(':')[-1]
            st4 = l[17].split(':')[-1]
            art = float(l[18].split(':')[-1]) / 1000000.0
            arc = l[19].split(':')[-1]
            query_comp[query_no+'-'+split+'-'+ss] = [jt1, jl1, jr1, jlr1, jc1, ct1, ct2, cm1, st1, st2, st3, st4, art, arc] + query_comp[query_no+'-'+split+'-'+ss]
        elif len(l) == 14:
            query_no = l[1].split(':')[-1]
            query_type = l[2].split(":")[1]
            split = l[3].split(':')[-1]
            ss = l[5].split(':')[-1]
            gss = int(l[4].split(':')[-1])-1
            iv1 = l[6].split(':')[-1]
            iv2 = l[7].split(':')[-1]
            av1 = l[8].split(':')[-1]
            av2 = l[9].split(':')[-1]
            te1 = l[10].split(':')[-1]
            te2 = l[11].split(':')[-1]
            ae1 = l[12].split(':')[-1]
            ae2 = l[13].split(':')[-1]
            if ae2 == '0':
                te2 = '0'
            if iv1 == '0' and iv2 == '0' and int(split) != nos[query_type]-2 and int(split) != 0:
                lines.append([query_no, query_type, split, ss, gss, 'splitj', iv1, av1, te1, ae1, 0, 0])
            if int(split) != nos[query_type]-1:
                if iv1 != '0':
                    lines.append([query_no, query_type, split, ss, gss, 'left', iv1, av1, te1, ae1, 0, 0])
            if int(split) == nos[query_type]-1:
                if iv1 != '0':
                    lines.append([query_no, query_type, split, ss, gss, 'right', iv1, av1, te1, ae1, 0, 0])
            if int(split) != 0 and int(split) != nos[query_type]-1:
                if iv2 != '0':
                    lines.append([query_no, query_type, split, ss, gss, 'right', iv2, av2, te2, ae2, 0, 0])

for i in lines:
    # if i[0] == '461':
    #     continue
    i[-2] = comp[i[0]+'-'+i[2]][0]
    i[-1] = comp[i[0]+'-'+i[2]][1]
    key = i[0]+'-'+i[2]+'-'+i[3]
    if key in query_comp:
        j=query_comp[key]
        i.append(j[0])
        i.append(j[1])
        i.append(j[2])
        i.append(j[3])
        i.append(j[4])
        i.append(j[5])
        i.append(j[8])
        i.append(j[9])
        i.append(j[10])
        i.append(j[11])
        i.append(j[12])
        i.append(j[13])
        i.append(j[14])

query_comp = {}

with open("C:\Users\Beast\Documents\IISc\Research\logs\\dec-01\\100k_f_500_cm1_comp.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(" ")
        t = float(l[11]) * 1000
        ss = int(l[18][:-1])
        if ss in query_comp:
            query_comp[ss] = max(query_comp[ss], t)
        else:
            query_comp[ss] = t


for i in range(len(lines)):
    query_no = lines[i][0]
    gss = lines[i][4]
    s = 0
    lines[i].append(query_comp[gss])
    if i > 0:
        lines[i].append(lines[i-1][-3])
    else:
        lines[i].append(0)

# lines = [["Query", "Type", "Split", "SS", "GS", "Side", "IV", "AV", "IE", "AE", "Time", "Result", "Init_Time", "Init_Count", "Comp_Time", "Comp_Count", "Scatter_Time", "Scatter_Count",
#          "Join_Time", "left_plus_right", "left_cross_right", "Join_Count",  "Tot_Comp_Time", "Total_Comp_Count", "Msg_Count", "Total_SS_Time",  "Input_Msg_Count"]] + lines

#
#
# for i in temp:
#     lines.append(temp[i])
#
with open('100k_f_500_cm1.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)