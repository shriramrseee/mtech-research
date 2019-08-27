import networkx as nx

g = nx.Graph()

edges = {}

with open('dataset/iCall/iCall.csv') as f:
    for _ in range(1):
        next(f)
    for l in f:
        line = l.split(',')
        u = int(line[2])
        v = int(line[3])
        if line[4] == 'Incoming':
            d = -1
            key = str(v)+'-'+str(u)
        else:
            d = 1
            key = str(u)+'-'+str(v)
        start = line[0].replace('"', '')
        end = line[1].replace('"', '')
        if key in edges:
            edges[key].add((start, end))
        else:
            edges[key] = {(start, end)}

    new_edges = []
    for k in edges:
        u = int(k.split('-')[0])
        v = int(k.split('-')[1])
        dates = []
        for i in edges[k]:
            dates.append(i)
        dates.sort()
        start = ''
        end = ''
        for i in dates:
            start = start + ',' + i[0]
            end = end + ',' + i[1]
        new_edges.append((u, v, {'start_time': start[1:], 'end_time': end[1:]}))

    g.add_edges_from(new_edges)

    for n in g.nodes.keys():
        g.nodes[n]['start_time'] = '1000-01-01 00:00:00'
        g.nodes[n]['end_time'] = '9999-01-01 00:00:00'


nx.write_graphml(g, 'iCall.ml')