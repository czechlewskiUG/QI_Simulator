import csv
import random
import networkx as nx
import matplotlib.pyplot as plt
nodesBegin=[]
nodesEnd=[]
edges=[]
with open('UKE_INFO_1700491040982.csv', newline='') as csvfile:
    line = csv.reader(csvfile, dialect='excel', delimiter=';', quotechar='|')
    for row in line:
        nodesBegin.append(int(row[0]))
        nodesEnd.append(int(row[4]))
        edges.append((int(row[0]),int(row[4]),float(row[17])))
G = nx.Graph()
G.add_nodes_from(nodesBegin)
G.add_nodes_from(nodesEnd)
G.add_weighted_edges_from(edges)
#nx.draw(G, with_labels=True, font_weight='bold')
nodeBeginRandom=random.choice(nodesBegin)
nodeEndRandom=random.choice(nodesBegin)
print('Number od nodes:',G.number_of_nodes())
print('Number od edges:',G.number_of_edges())
#print('Random node begin:',nodeBeginRandom)
#print('Random node end:',nodeEndRandom)
#print(nx.dijkstra_path(G, nodeBeginRandom, nodeEndRandom))
print(nx.dijkstra_path(G, 6837743,6563274))
#plt.show()

