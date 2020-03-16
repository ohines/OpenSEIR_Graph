## SIR model on a networkx Graph object
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import compress

class Population:
    def __init__(self,G):
        self.G = G
        self.params = {'pTransmitE' : 0.02, 'pTransmitI' : 0.05}
        N = G.number_of_nodes()
        self.N = N
        self.active_nodes = range(N)
        self.S = [True]*N
        self.E = [False]*N
        self.I = [False] * N
        self.R = [False] * N
        self.Time = 0 #World time in days
        self.Etime = [0]*N #Exposure time initialised to zero
        self.Itime = [0]*N #Infectious time initialised to zero
        self.Incubation = [4]*N #Duration between E and I (could be randomised in later versions)
        self.Iduration = [10]*N #Duration unitl recovery (could be randomised in later versions)
        self.seed_infection(0)
        self.SIR_stats = {'S':[sum(self.S)], 'E':[sum(self.E)] ,'I':[sum(self.I)], 'R':[sum(self.R)], 'T':[0]}
        self.dynamic = any(self.I)

    def advance_day(self):
        if self.dynamic:
            self.Time += 1
            S = self.S
            E = self.E
            I = self.I
            for i in self.active_nodes:
                neighbors = list(nx.neighbors(self.G, i))
                if S[i]:
                    I_neighbors = sum(map(I.__getitem__, neighbors)) #number of infected neighbors
                    E_neighbors = sum(map(E.__getitem__, neighbors))
                    new_infections = (np.random.binomial(I_neighbors,self.params['pTransmitI']) +
                                      np.random.binomial(E_neighbors, self.params['pTransmitE']))
                    if new_infections >=1:
                        self.expose_person(i)
                if E[i]:
                    if self.Time - self.Etime[i] >= self.Incubation[i]:
                        self.infect_person(i)
                if I[i]:
                    if self.Time - self.Itime[i] >= self.Iduration[i]:
                        self.remove_person(i)
                self.intervention()
            #update stats
            self.SIR_stats['S'].append(sum(self.S))
            self.SIR_stats['E'].append(sum(self.E))
            self.SIR_stats['I'].append(sum(self.I))
            self.SIR_stats['R'].append(sum(self.R))
            self.SIR_stats['T'].append(self.Time)
            self.dynamic = any(self.I) or any(self.E)

    def propogate(self,pTrue=False,Ndays=1000):
        while self.Time < Ndays and self.dynamic:
            self.advance_day()
            if pTrue:
                self.plot_Network_status()
                plt.show()

    def expose_person(self,i):
        self.S[i],self.E[i],self.I[i],self.R[i] = False , True , False, False
        self.Etime[i] = self.Time

    def infect_person(self,i):
        self.S[i], self.E[i], self.I[i], self.R[i] = False, False, True, False
        self.Itime[i] = self.Time

    def remove_person(self,i):
        self.S[i], self.E[i], self.I[i], self.R[i] = False, False, False, True

    def seed_infection(self,i):
        self.infect_person(i)

    def intervention(self):
        # Place holder method where an intervention may be defined which is carried out each time step.
        pass

    def get_summary(self,pcrit):
        prop = np.array(self.SIR_stats['I'])/self.N
        return [max(prop),sum(prop>=pcrit)]

    def plot_SIR_stats(self):
        df = pd.DataFrame(self.SIR_stats)/self.N
        df['T'] = self.SIR_stats['T']
        ax = df.plot(y=['I','E','S','R'],x='T',kind='bar',stacked=True,width=1,
                     xticks=range(0,self.Time,10),ylim=(0,1))#,edgecolor='black')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Population proportion')
        ax.tick_params(axis='x', rotation=0)

    def plot_Network_status(self): #Only to be used for small networks
        def get_col(x):
            z = ['red','orange','blue','green']
            return(list(compress(z, x))[0])

        cols = [get_col(x) for x in zip(self.S,self.E,self.I,self.R)]
        nx.draw_circular(self.G,node_size=150,node_color=cols)
        #maybe plot degree distribution also


