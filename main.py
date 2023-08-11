from copy import deepcopy

from src.simulation import Sim
from src.parameter import hhold_nw
from src.parameter import school_nw
from src.parameter import work_nw
from src.parameter import daycare_nw
from src.parameter import DAYS

if __name__ == '__main__':
    aSim = Sim()
    print ("Simulation Starts...")
    #Network
    H = deepcopy(hhold_nw)
    W = deepcopy(work_nw)
    S = deepcopy(school_nw)
    D = deepcopy(daycare_nw)

    SEIR, Multi_SEIR, Spread_Tree = aSim.Run(H, W, S, D, DAYS)
    print("Simulation Done~")
    print("==============================")
    print("Saving Results~")
    SEIR.to_csv('test_overall_disease_dynamic.csv')
    Multi_SEIR.to_csv('test_multi_disease_dynamic.csv')
    Spread_Tree.to_csv('test_tracing.csv')
    print("Done!~")


