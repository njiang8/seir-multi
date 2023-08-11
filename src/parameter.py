import pandas as pd
import networkx as nx

#Sample Population
pop = pd.read_csv('Data/erie-data/Erie_pop_id.csv').iloc[:,1:]#.set_index('id')
print('Total population in ERIE County is:', len(pop))

#Networks"
#hhold_networks
hhold_nw = nx.read_adjlist('Data/erie-data/networks/hhold_nw.csv', delimiter=',')
#daycare
daycare_nw = nx.read_adjlist('Data/erie-data/networks/daycare_nw.csv', delimiter=',')
#school
school_nw = nx.read_adjlist('Data/erie-data/networks/school_nw.csv', delimiter=',')
#work
work_nw = nx.read_adjlist('Data/erie-data/networks/work_nw.csv', delimiter=',')


# Number of agents
N = len(pop)
print("Population size", N)

#Number of Infected at the beginning of the simulation
NI = 2
print("Total Infected or Exposed people at the beginning", NI)

#Introduce New Thred or Not
INTRO = False
if INTRO == True:
    print("Running Multi Disease Model...")

#Number of Days
DAYS = 150
#DAYS = 120
print("Simulation of ", DAYS, "days")