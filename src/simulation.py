import os
import pandas as pd
from loguru import logger

from src.seir import World
from src.setting_simulation_results_path import LOC_PATH_RESULT


class Sim(object):
    def __init__(self, population):
        self.World = World(population_size=len(population))
        self.df = pd.DataFrame([])

    def Run(self,populatoin,
            hhold_nx, work_nx, school_nx, daycar_nx,
            DAYS, INTRO, TRACK, THREAD):

        steps = DAYS * 3
        logger.info(f"-Simulation->Run->Simulation steps: {steps}")
        #Num_Population = len()
        id_d = self.World.__initialize_agents__(populatoin,
                                                hhold_nx, work_nx, school_nx, daycar_nx,
                                                THREAD)  # create fullpop with pop dataset

        SEIR_Results = []
        Multi_SEIR = []
        Location = []
        track = pd.DataFrame()
        #loc_tract = []

        day = 0
        for i in range(0, steps):


            if i % 3 == 0:
                '''
                1.Collect data
                '''
                #Get exposed population
                e_time, ids, wheres, froms = self.World.track_exposed_history(day)
                #temp = pd.DataFrame([ids, wheres, froms], columns=['target', 'where', 'source']).T
                temp = pd.DataFrame([e_time, ids, wheres, froms]).T
                track = pd.concat([track,temp])

                t, x1, x2, x3, x4, x5 = self.World.Update_SEIR(day)
                SEIR_Results.append([t, x1, x2, x3, x4, x5])

                if INTRO == True:
                    t, s, x, x1, x2, y, y1, y2, z, z1, z2, d = self.World.Update_SEIR_List(day)# Update SEIR
                    Multi_SEIR.append([t, s, x, x1, x2, y, y1, y2, z, z1, z2, d])

                # Get Infected Location
                time, h, w, d, s = self.World.Get_Location(day)
                Location.append([time, h, w, d, s])
                '''
                2.Main function
                '''
                if INTRO == True:
                    self.World.change_back_to_s() #change back to s
                    self.World.Home_Spread(id_d, day)  # spread disease
                    self.World.Recover()  # recovery
                    self.World.Intro_New_Thread(day,INTRO)  # intro new disease INTRO is the global parameter to control
                else:
                    self.World.Home_Spread(id_d, day)  # spread disease
                    self.World.Recover()  # recovery
                    self.World.Intro_New_Thread(day, INTRO)  # intro new disease INTRO is the global parameter to control

                day = day + 1  # update simulation day

                if day % 10 == 0:
                    logger.info(f"Current Day: {day}")
                    if TRACK == True:
                        tract_location_path = os.path.join(LOC_PATH_RESULT, f"wny_tract_R0_{THREAD}_df_{day}.csv")
                        loc_track_df = self.World.get_infected_population(day)
                        loc_track_df.to_csv(tract_location_path)
                        #loc_track_df.to_csv("../results/west_ny/wny_track_df" + str(day) + ".csv")
                    #print("simulation-> get infectd id", loc_track_df.head())


            elif i % 3 == 1:
                # print("Day:", day,"Daytime")
                self.World.Work_Spread(id_d, day)
                self.World.Recover()

            elif i % 3 == 2:
                # print("Day:", day,"Evening")
                self.World.Home_Spread(id_d, day)
                self.World.Recover()
        #Overall SEIR
        df1 = pd.DataFrame(SEIR_Results,
                           columns=['Day', 'S', 'E', 'I', 'R', 'D']
                           )

        # Multi SEIR
        df2 = pd.DataFrame(Multi_SEIR,
                           columns=['Day', 'S', 'E', 'E1', 'E2', 'I', 'I1', 'I2', 'R', 'R1', 'R2', 'D'])
        # Location
        #df2 = pd.DataFrame(Location, columns=['Day', 'Home', 'Work', 'Daycare', 'School'])

        return df1, df2, track