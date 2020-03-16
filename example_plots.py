
from model import *

G = nx.barabasi_albert_graph(5000,2,seed=1234)
a = Population(G)
a.propogate()
a.plot_SIR_stats()
#plt.savefig('plots/BA_example.png')

H = nx.powerlaw_cluster_graph(5000,2,0.85,seed=1234)
b = Population(H)
b.propogate()
b.plot_SIR_stats()
#plt.savefig('plots/Power_cluster_example.png')

print(nx.number_of_nodes(G),nx.number_of_nodes(H))
print(nx.number_of_edges(G),nx.number_of_edges(H))


