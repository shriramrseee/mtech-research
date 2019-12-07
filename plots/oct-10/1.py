import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import datetime

temp = {}

with open("C:\Users\Beast\Documents\IISc\Research\logs\oct-11\\2\\10k_zf.log") as f:
    skip = 0
    old = 0
    for line in f:
        l = line[:-1].split(",")
        print l
        if len(l) == 6:
            # skip first two
            skip += 1
            if skip > 1:
                # get time, msg, query no and type
                etime = int(l[-1].split(":")[-1])
                msg = int(l[-2].split(":")[-1])
                query_no = int(l[1].split(':')[-1])
                query_type = l[2].split(":")[1]
                if l[3] == 'Superstep:-1':
                    # Start new query
                    temp[query_no] = [query_type, etime, etime, msg, 0]
                    old = query_no
                else:
                    # Update query stats
                    temp[old][2] = etime
                    temp[old][3] += msg
        elif len(l) == 4:
            if l[-1].split(':')[0] == 'Result Size':
                temp[old][4] = int(l[-1].split(":")[1])


qtypes = {'query_3': 0, 'query_4': 1, 'query_5': 2, 'query_6': 3, 'query_7': 4}
exectime = [0 for i in qtypes]
messages = [0 for i in qtypes]
result = [0 for i in qtypes]
count = [0 for i in qtypes]

for i in temp:
    exectime[qtypes[temp[i][0]]] += temp[i][2] - temp[i][1]
    messages[qtypes[temp[i][0]]] += temp[i][3]
    result[qtypes[temp[i][0]]] += temp[i][4]
    count[qtypes[temp[i][0]]] += 1

for i in qtypes:
    if count[qtypes[i]] != 0:
        exectime[qtypes[i]] /= count[qtypes[i]] * 1000.0
        messages[qtypes[i]] /= count[qtypes[i]] * 1.0
        result[qtypes[i]] /= count[qtypes[i]] * 1.0

xval = [i for i in qtypes]
xval.sort()

# exectime[4] = 0
# messages[4] = 0


fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6, 12))
axes[0].bar(xval, exectime, zorder=3)
axes[1].bar(xval, messages, zorder=3, color="green")
axes[2].bar(xval, result, zorder=3, color="orange")
# plt.yscale("log")
axes[1].set_yscale("log")
axes[2].set_yscale("log")
axes[0].set_ylim(ymax=100)
axes[1].set_ylim(ymax=1000000)
axes[2].set_ylim(ymin=0.1)
axes[2].set_ylim(ymax=100000)
axes[0].set_ylabel("Avg. Exec Time (s)")
axes[1].set_ylabel("Avg. Total Messages (log)")
axes[2].set_ylabel("Avg. Result Count (log)")
# axes[0].set_title('10k_dw V:5,569,812 E: 20,869,581 - Query - Result', fontsize=10)
# axes[0].set_title('10k_f V:2,831,428 E: 9,152,392 - Query - Result', fontsize=10)
axes[0].set_title('10k_zf V:1,078,032 E: 2,420,032 - Query - Result', fontsize=10)
# axes.legend(['Male', 'Female'])
plt.xlabel('Query Type')
# plt.ylabel('Count (log scale)')
# plt.xticks(xval3, xticks)
axes[0].grid(which='both', zorder=0)
axes[1].grid(which='both', zorder=0)
axes[2].grid(which='both', zorder=0)
plt.minorticks_on()
plt.show()
