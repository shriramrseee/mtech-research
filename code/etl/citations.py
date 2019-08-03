import networkx as nx

g = nx.Graph()

edges = []
nodes = []

with open('dataset/tCitation/hep-th-slacdates') as f:
    for l in f:
        line = l.split(' ')
        nodes.append((int(line[0]), {'start_time': line[1], 'end_time': '9999-01-01'}))
    g.add_nodes_from(nodes)

with open('dataset/tCitation/hep-th-citations') as f:
    for l in f:
        line = l.split(' ')
        start = g.node[int(line[0])]['start_time']
        edges.append((int(line[0]), int(line[1]), {'start_time': start, 'end_time': '9999-01-01'}))
    g.add_edges_from(edges)

nx.write_graphml(g, 'tCitations.ml')