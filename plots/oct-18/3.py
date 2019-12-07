import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-18\\10k_f_cost.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        print len(l), l
        if len(l) == 9:
            query_no = l[1].split('-')[-1].strip()
            query_split = l[2].split(":")[1]
            pred_index = l[3].split(":")[1]
            mpv = l[4].split(":")[1]
            av = l[5].split(":")[1]
            vd = l[6].split(":")[1]
            ef = l[7].split(":")[1]
            oe = l[8].split(":")[1]
            key = query_no + '-' + query_split
            if key in temp:
                temp[key].append([pred_index, mpv, av, vd, ef, oe])
            else:
                temp[key] = [[pred_index, mpv, av, vd, ef, oe]]

lines = []

for i in temp:
    k = i.split("-")
    v = temp[i]
    for j in range(0, len(v)):
        lines.append([k[0], k[1], v[j][0], v[j][1], v[j][2], v[j][3], v[j][4], v[j][5]])

with open('10k_F_split_cost.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)

qtypes = {'query_3': 0, 'query_4': 1, 'query_5': 2, 'query_6': 3, 'query_7': 4}
exectime = [0 for i in qtypes]
messages = [0 for i in qtypes]
result = [0 for i in qtypes]
count = [0 for i in qtypes]

# for i in temp:
#     exectime[qtypes[temp[i][0]]] += temp[i][2] - temp[i][1]
#     messages[qtypes[temp[i][0]]] += temp[i][3]
#     result[qtypes[temp[i][0]]] += temp[i][4]
#     count[qtypes[temp[i][0]]] += 1
#
# for i in qtypes:
#     if count[qtypes[i]] != 0:
#         exectime[qtypes[i]] /= count[qtypes[i]] * 1000.0
#         messages[qtypes[i]] /= count[qtypes[i]] * 1.0
#         result[qtypes[i]] /= count[qtypes[i]] * 1.0
#
# xval = [i for i in qtypes]
# xval.sort()
#
# # exectime[4] = 0
# # messages[4] = 0
#
#
# fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6, 12))
# axes[0].bar(xval, exectime, zorder=3)
# axes[1].bar(xval, messages, zorder=3, color="green")
# axes[2].bar(xval, result, zorder=3, color="orange")
# # plt.yscale("log")
# axes[1].set_yscale("log")
# axes[2].set_yscale("log")
# axes[0].set_ylim(ymax=100)
# axes[1].set_ylim(ymax=1000000)
# axes[2].set_ylim(ymin=0.1)
# axes[2].set_ylim(ymax=100000)
# axes[0].set_ylabel("Avg. Exec Time (s)")
# axes[1].set_ylabel("Avg. Total Messages (log)")
# axes[2].set_ylabel("Avg. Result Count (log)")
# # axes[0].set_title('10k_dw V:5,569,812 E: 20,869,581 - Query - Result', fontsize=10)
# # axes[0].set_title('10k_f V:2,831,428 E: 9,152,392 - Query - Result', fontsize=10)
# axes[0].set_title('10k_zf V:1,078,032 E: 2,420,032 - Query - Result', fontsize=10)
# # axes.legend(['Male', 'Female'])
# plt.xlabel('Query Type')
# # plt.ylabel('Count (log scale)')
# # plt.xticks(xval3, xticks)
# axes[0].grid(which='both', zorder=0)
# axes[1].grid(which='both', zorder=0)
# axes[2].grid(which='both', zorder=0)
# plt.minorticks_on()
# plt.show()
