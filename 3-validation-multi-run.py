import os
import timeit
from loguru import logger

import pandas as pd
import networkx as nx
from copy import deepcopy

from src.simulation import Sim
from src.setting_simulation_results_path import RESULT_PATH


#Sample Population
print("--Parameter->read population..")
start_time = timeit.default_timer()

population = pd.read_csv('data/input/Western_NY/population/wny_pop.csv').iloc[:, 1:]#.set_index('id')
print('---Populatoin reading ended ({:.1f} secs)'.format(timeit.default_timer() - start_time))
print('---Total population is:', len(population))

#Networks"
print("--Parameter->read Social Networks..")
start_time = timeit.default_timer()
#hhold_networks
print("---Parameter->read Household Networks..")
hhold_nw = nx.read_adjlist('data/input/Western_NY/population/wny_hhold_nw.csv', delimiter=',')
#print('Hhold NW reading ended ({:.1f} secs)'.format(timeit.default_timer() - start_time))
#daycare
print("--Parameter->read Daycare Networks..")
daycare_nw = nx.read_adjlist('data/input/Western_NY/population/wny_daycare_nw.csv', delimiter=',')
#print('Daycare NW reading ended ({:.1f} secs)'.format(timeit.default_timer() - start_time))
#school
print("--Parameter->read School Networks..")
school_nw = nx.read_adjlist('data/input/Western_NY/population/wny_school_nw.csv', delimiter=',')
#print('School Nw reading ended ({:.1f} secs)'.format(timeit.default_timer() - start_time))
#work
print("--Parameter->read Work Networks..")
work_nw = nx.read_adjlist('data/input/Western_NY/population/wny_work_nw.csv', delimiter=',')
#print('Work reading ended ({:.1f} secs)'.format(timeit.default_timer() - start_time))
print('---Network reading ended ({:.1f} secs)'.format(timeit.default_timer() - start_time))

DAYS  = 150 #set the overall simulation steps: simulation steps = DAYS * 3
INTRO = False # if introduce another thread make the model simulate two thread of disease
TRACK = False # if track the seir location

thread_list = [1 ,2, 3] # the thread number thread1: r0 = 3; thread2: r0 = 5; thread3: r0 = 8

if __name__ == '__main__':
    logger.info(f"Simulation starts...")

    # logger.info(f"loading networks...")
    # # load Networks
    # hhold_nw_input = deepcopy(hhold_nw)
    # work_nw_input = deepcopy(work_nw)
    # school_nw_input = deepcopy(school_nw)
    # daycare_nw_input = deepcopy(daycare_nw)

    for THREAD_NUM in thread_list:
        logger.info(f"Simulation:Thread {THREAD_NUM}")
        multi_run_df = pd.DataFrame()
        for run in range(10): #set how many time you would like to resun the simulation
            aSim = Sim(population)
            logger.info(f"Simulation Run {run} starts...")
            try:
                SEIR, Loc, Spread_Tree = aSim.Run(population, hhold_nw, work_nw, school_nw,
                                                  daycare_nw, DAYS, INTRO, TRACK, THREAD_NUM)
                SEIR['Run'] = run  # Add a column to indicate the run number

                logger.info(f"Run {run} Done~")
                multi_run_df = pd.concat([multi_run_df, SEIR], ignore_index=True)
            except Exception as e:
                logger.error(f"Error in Run {run}: {e}")

            # multi_run_df = pd.concat([multi_run_df, SEIR], ignore_index=True)
        # Make sure the directory exists; if not, create it
        if not os.path.exists(RESULT_PATH):
            os.makedirs(RESULT_PATH)

        multi_run_df_path = os.path.join(RESULT_PATH, f"multi_run_results_r{THREAD_NUM}.csv")
        logger.info(f"Saving results to {multi_run_df_path}")
        multi_run_df.to_csv(multi_run_df_path)

    logger.info("Simulation Runs Done!")