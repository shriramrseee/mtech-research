#!/usr/bin/python

import pandas as pd
import numpy as np
import matplotlib
import os

matplotlib.use('Agg')  # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import sys
import os.path
from pylab import *

'''
    Usage :

        python vPlot.py Input-File Out-File xAxis-HeaderLabels X-Axis_Title Y-Axis_Title

    xAxis-HeaderLabels should be comma separated values.

        python vPlot_cep.py C:\Users\Beast\Documents\IISc\Dream\cofee\exp\index_mb_logs\cep_10_100_1/cep.csv cep.pdf "          10,.                                   100" "DAG Count" "Latency (ms)" 0

'''

# Array Declarations
mean = []
medians = []
plotMap = []
xheaderTicks = []
xheaderLabels = [x.strip('.') for x in sys.argv[3].split(',')]
xHeaderLabelAngle = long(sys.argv[6])
indexes_to_take = []
indexes_to_drop = []
maxArray = []

# Use below parameter in pandas to ignore columns
# usecols=["date", "loc", "x"]

# Accepts InputFile for processing
inputFile = pd.read_csv(sys.argv[1], engine='python', header=None, encoding='utf-8-sig')

for i in range(len(xheaderLabels)):
    plotMap.append(inputFile[i].dropna().tolist())
    xheaderTicks.append(i + 1)

# Prints Summary of InputFile
print("\nInput File Summary: \n")
print(inputFile.describe())

# Creates Figure Instance
plt.ticklabel_format(useOffset=False)
plt.ticklabel_format(style='plain')
plt.grid(which='minor', alpha=0.5)
plt.grid(which='major', alpha=0.5)
fig = plt.figure(1, figsize=(12, 6))

# Create an Axes Instance
ax = fig.add_subplot(111)

# Create the boxplot
bp = ax.violinplot(plotMap, showmedians=True, showmeans=True, showextrema=True)
bp['cmeans'].set_color('b')
bp['cmedians'].set_color('g')

# pc_color = ['#00a8ff', '#f195ac', '#00a8ff', '#f195ac']
#
# for i in range(0, len(xheaderLabels)):
#     bp['bodies'][i].set_facecolor(pc_color[i])
#     bp['bodies'][i].set_edgecolor('k')
#     bp['bodies'][i].set_alpha(1)

pltno = 1

# Vice-City Color Pallete http://www.color-hex.com/color-palette/45584
for pc in bp['bodies']:
    if(pltno % 8 ==0):
        pc.set_facecolor('#00a8ff')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==1):
        pc.set_facecolor('#0266c8')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==2):
        pc.set_facecolor('#f195ac')
        pc.set_edgecolor('black')
    elif(pltno % 8 ==3):
        pc.set_facecolor('#b28bc0')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==4):
        pc.set_facecolor('#7fd13b')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==5):
        pc.set_facecolor('#c64847')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==6):
        pc.set_facecolor('#005bd3')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    else:
        pc.set_facecolor('#c64847')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    pltno+=1

# Axis Header
# ax.set_ylim(ymin=0)
# ax.set_yscale('log')
# ax.set_ylim(ymin=1)
# ax.set_ylim(ymax=10e5)
# ax.set_xticks([1.5, 2.5, 3.5, 4.5])
ax.set_xticklabels(xheaderLabels, size=16, rotation=xHeaderLabelAngle)
ax.set_xlabel(sys.argv[4], size=16)
ax.set_ylabel(sys.argv[5], size=16)
ax.yaxis.grid(which='major', alpha=0.5)
ax.set_xticks(xheaderTicks)
ax.set_title(sys.argv[7], size=20)
# ax.legend(['0.1% Match', '1% Match'], loc='upper left')
ax.minorticks_on()

######################################################################
###########            Plot Computation Begins          ##############
######################################################################

# Appends Mean and Median for each Column to Array
for i in range(0, len(xheaderLabels)):
    mean.append(sum(inputFile[i].dropna().tolist()) / len(inputFile[i].dropna().tolist()))
    medians.append(median(inputFile[i].dropna().tolist()))

# Writing Median values
for i in range(1, len(medians) + 1):
    text(i, medians[i - 1], '%.1f' % medians[i - 1], horizontalalignment='right', color='red', size=12)

# Writing Mean values
for i in range(1, len(mean) + 1):
    text(i, mean[i - 1], '%.1f' % mean[i - 1], horizontalalignment='left', color='purple', size=12)

# Marking Median with custom symbol
inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='o', color='white', s=15, zorder=3)

# Graph Annotation
# plt.annotate('', (0,0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')

# Appends Quantile Info of Printing
quantile25 = []
quantile75 = []

for i in range(0, len(xheaderLabels)):
    quantile25.append(np.percentile([inputFile[i].dropna().tolist()], [25], axis=1)[0])
    quantile75.append(np.percentile([inputFile[i].dropna().tolist()], [75], axis=1)[0])

inds = np.arange(1, len(medians) + 1)
# ax.vlines(inds, quantile25, quantile75, color='k', linestyle='-', lw=5)

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(7.5, 3)

######################################################################
###########            Plot Computation Ends          ################
######################################################################

# Save the figure
fig.savefig(sys.argv[2], bbox_inches='tight')
print("\n[SUCCESS] : Plot generated Successfully!")
print("[PATH] : " + sys.argv[2])

# python vPlot_neo4j.py 10k_dw_neo4j_query_3.csv 10k_dw_neo4j_query_3.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "10k_dw - Q3 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 10k_dw_neo4j_query_6.csv 10k_dw_neo4j_query_6.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "10k_dw - Q6 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 10k_dw_neo4j_query_4.csv 10k_dw_neo4j_query_4.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "10k_dw - Q4 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 10k_dw_neo4j_query_7.csv 10k_dw_neo4j_query_7.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "10k_dw - Q7 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 10k_dw_neo4j_query_23.csv 10k_dw_neo4j_query_23.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "10k_dw - Q23 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 10k_dw_neo4j_query_9.csv 10k_dw_neo4j_query_9.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "10k_dw - Q9 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 10k_dw_neo4j_query_11.csv 10k_dw_neo4j_query_11.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "10k_dw - Q11 - Neo4J - Exec. Time"

# python vPlot_neo4j.py 100k_zf_neo4j_query_3.csv 100k_zf_neo4j_query_3.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_zf - Q3 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_zf_neo4j_query_6.csv 100k_zf_neo4j_query_6.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_zf - Q6 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_zf_neo4j_query_4.csv 100k_zf_neo4j_query_4.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_zf - Q4 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_zf_neo4j_query_7.csv 100k_zf_neo4j_query_7.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_zf - Q7 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_zf_neo4j_query_23.csv 100k_zf_neo4j_query_23.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_zf - Q23 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_zf_neo4j_query_9.csv 100k_zf_neo4j_query_9.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_zf - Q9 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_zf_neo4j_query_11.csv 100k_zf_neo4j_query_11.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_zf - Q11 - Neo4J - Exec. Time"


# python vPlot_neo4j.py 100k_a_neo4j_query_3.csv 100k_a_neo4j_query_3.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_a - Q3 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_a_neo4j_query_6.csv 100k_a_neo4j_query_6.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_a - Q6 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_a_neo4j_query_4.csv 100k_a_neo4j_query_4.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_a - Q4 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_a_neo4j_query_7.csv 100k_a_neo4j_query_7.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_a - Q7 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_a_neo4j_query_23.csv 100k_a_neo4j_query_23.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_a - Q23 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_a_neo4j_query_9.csv 100k_a_neo4j_query_9.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_a - Q9 - Neo4J - Exec. Time"
# python vPlot_neo4j.py 100k_a_neo4j_query_11.csv 100k_a_neo4j_query_11.pdf "Cypher,Gremlin" "Split/CM" "Exec. Time (ms)" 0 "100k_a - Q11 - Neo4J - Exec. Time"





