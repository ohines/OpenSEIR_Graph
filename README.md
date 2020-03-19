# Open SEIR Graph: A project investigating population structure interventions on epidemic dynamics


## Introduction

This open project is inspired by the Covid-19 epidemic of 2020, with the aim of studying the
effect of underlying social structure on epidemic dynamics. The project intends to qualitatively model
the effect of various social structure interventions (lockdowns, quarantines, isolation, social-distancing)
on the dynamics of disease spread. 

The basic model for this study is an [SEIR (Susceptible, Exposed, Infectious,Removed) model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#Elaborations_on_the_basic_SIR_model) 
built on a graphical population structure. [See related theoretical work](https://link.springer.com/content/pdf/10.1007/s00285-019-01329-4.pdf).
The most realistic models of the Covid-19 outbreak, such as those by the 
[Imperial College Covid-19 response team](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf)
use spatial modelling to simulate a population with realistic demographic characteristics. Simulated
individuals are then exposed to the infection by co-located individuals with some transmission probability,
and the state of individuals is updated in discrete time steps.

The current project aims to replicate the qualitative behaviour observed by the group at Imperial, using a complex system with a 
significantly simpler rule and parameter set. In our model, a population is simulated according to a random graph generator,
with nodes representing people, and edges representing social contacts between two people.
The infection will then be allowed to spread from infected nodes to susceptible nodes along edges with some transmission 
probability, and the disease status of each node in discrete time steps.

In this simplified world, interventions can be understood as dynamic updates to the underlying population structure.
The model is built in python using the `networkx` python package to represent graph structure.
Model code can be found in `model.py`, with technical details regarding the model given in `Papers/Model_details.pdf`.
Estimands of interest, and methods for obtaining Monte Carlo estimates, are discussed in the same document. 


## Illustrative Example

As an example of the effect of population structure we consider two populations, of 5000
people, the first of which is generated according to the [Barabási–Albert (BA)](https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model)
preferential attachent model, the second generated according to a [Power law cluster (PLC)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.65.026107)
model. The PLC graph grows according to preferential attachment, but has an additional 
step which makes clique formation more likely.

These two graph types were chosen as they reasonably replicate the scale free behaviour observed in naturally occuring
social structures, with the second also replicating clique-like behaviour. The source code for this example is found in 
`example_plots.py`. Epidemics were set up with a single intial infectious person (patient 0).

For this illustration, an incubation period of 4 days was assumed, during which the probability of transmission to a susceptible person along an edge on a given day
was 0.01. This was followed by an infectious period of 10 days during which the probability of transmission
was 0.05 for each day. Two realisations of such a epidemic on the BA and PLC graphs are shown by the two figures below.
Both graphs contained 9996 edges (social connections).

![An example epidemic on a BA population](plots/BA_example.png)

![An example epidemic on a PLC population](plots/Power_cluster_example.png)

To investigate the effect of this structural difference on the maximum proportions of infections
a Monte Carlo simulation can be run, the code for which can be found in `Monte_Carlo_estimator.py`.
For this particular example, across 100 MC simulations from each model we approximate the expected 
maximum infection proportion to be 0.254±0.001 and 0.195±0.001, suggesting that greater clustering of
the social contact graph may significantly reduce the peak number of infections during the epidemic.

## Future work

At this stage this project is very much in its infancy, however collaborators may 
direct future work to the following areas:
* How can the SEIR model be modified to more accurately reflect transmission observations. This may include adding strucutre to reflect age and comorbidities.
* What graphical structure best represents that of real social contact? To what extent
are conclusions about intervention measures sensitive to the underlying graphical strucutre?
* What is the effect of dynamic interventions? These may include rules
such as removing edges from infecting individuals (e.g. quarantine), removing edges from certian 
individuals for a limited number of days (e.g. lockdown, social-distancing)


