import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}
temp1 = {}

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-18\\10k_f.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        print l
        if len(l) == 7:
            print l
            # skip first two
            skip += 1
            if skip > 1:
                # print l
                # get time, msg, query no and type
                etime = int(l[-1].split(":")[-1])
                msg = int(l[-2].split(":")[-1])
                query_no = l[1].split(':')[-1]
                query_split = l[2].split(":")[1]
                query_type = l[3].split(":")[1]
                if l[4] == 'Superstep:-1':
                    # Start new query
                    old = query_no+'-'+query_split+'-'+query_type
            else:
                continue
        if len(l) == 16:
            query_no = l[1].split(':')[-1]
            query_split = l[2].split(":")[1]
            if query_split == 'null':
                continue
            query_type = l[3].split(":")[1]
            query_superstep = l[4].split(":")[1]
            mpv1 = l[5].split(":")[1]
            cv1 = l[6].split(":")[1]
            pv1 = l[7].split(":")[1]
            pe1 = l[8].split(":")[1]
            vod1 = l[9].split(":")[1]
            vid1 = l[10].split(":")[1]
            om1 = l[11].split(":")[1]
            it = l[12].split(":")[1]
            ct = l[13].split(":")[1]
            st = l[14].split(":")[1]
            tt = l[15].split(":")[1]
            key = old + '-' + 'left'
            if key in temp:
                temp[key].append([query_superstep, mpv1, cv1, pv1, pe1, vod1, vid1, om1, it, ct, st, tt])
            else:
                temp[key] = [[query_superstep, mpv1, cv1, pv1, pe1, vod1, vid1, om1, it, ct, st, tt]]
        elif len(l) == 12:
            query_no = l[1].split(':')[-1]
            query_split = l[2].split(":")[1]
            if query_split == 'null':
                continue
            query_type = l[3].split(":")[1]
            query_superstep = l[4].split(":")[1]
            mpv1 = l[5].split(":")[1]
            cv1 = l[6].split(":")[1]
            pv1 = l[7].split(":")[1]
            pe1 = l[8].split(":")[1]
            vod1 = l[9].split(":")[1]
            vid1 = l[10].split(":")[1]
            om1 = l[11].split(":")[1]
            key = old + '-' + 'right'
            if key in temp:
                temp[key].append([query_superstep, mpv1, cv1, pv1, pe1, vod1, vid1, om1, 0, 0, 0, 0])
            else:
                temp[key] = [[query_superstep, mpv1, cv1, pv1, pe1, vod1, vid1, om1, 0, 0, 0, 0]]
                         

s = ['2', '1', '1', '2', '3']

lines = []

for i in temp:
    k = i.split("-")
    v = temp[i]
    index = 0
    if k[1] == '0' or s[int(k[2].split('_')[1])-3] == k[1]:
        if k[3] == 'right':
            continue

    skip = {0, len(v)-3, len(v) - 2, len(v) - 1}

    for j in range(0, len(v)):
        if j in skip:
            continue
        lines.append([k[0], k[1], k[2], k[3], index, v[j][1], v[j][2], v[j][3], v[j][4], v[j][5], v[j][6], v[j][7], v[j][8], v[j][9], v[j][10], v[j][11]])
        index += 1

with open('10k_F_split_actual.csv', 'wb') as writeFile:
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
