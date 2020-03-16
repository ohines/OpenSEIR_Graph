# File which generates Monte Carlo (MC) estimates of
# the max Infection intensity (Imax)

from model import *


def MC_pandemic_samples(Pop_generator,N_it=100):
    it = 0
    Imax = []
    while it <= N_it:
        a = Pop_generator()
        a.propogate()
        Imax.append(a.get_summary(0.1)[0])
        it += 1
    return(Imax)


def P_BA():
    G = nx.barabasi_albert_graph(5000,2,seed=1234)
    return(Population(G))

def P_PLC():
    G = nx.powerlaw_cluster_graph(5000, 2, 0.85,seed=1234)
    return(Population(G))

N_mc = 100
BA_samps = MC_pandemic_samples(P_BA,N_mc)
PLC_samps = MC_pandemic_samples(P_PLC,N_mc)

#MC estimate
print(np.mean(BA_samps)) #0.25411881188118807
print(np.mean(PLC_samps)) #0.19511683168316826

#MC error
print(np.std(BA_samps)/N_mc**0.5) #0.0009686580621299144
print(np.std(PLC_samps)/N_mc**0.5) #0.001463405136210404