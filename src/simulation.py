import pandas as pd
from src.seir import World
from src.parameter import pop

class Sim(object):
    def __init__(self):
        self.World = World()
        self.df = pd.DataFrame([])

    def Run(self, H, W, S, D, DAYS):
        steps = DAYS * 3
        print("Simulation steps:", steps)

        id_d = self.World.__initialize_agents__(pop, H, W, S, D)  # create fullpop with pop dataset

        SEIR_Results = []
        Multi_SEIR = []
        Location = []
        track = pd.DataFrame()

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

                t, s, x, x1, x2, y, y1, y2, z, z1, z2, d = self.World.Update_SEIR_List(day)# Update SEIR
                Multi_SEIR.append([t, s, x, x1, x2, y, y1, y2, z, z1, z2, d])

                # Get Infected Location
                time, h, w, d, s = self.World.Get_Location(day)
                Location.append([time, h, w, d, s])
                '''
                2.Main function
                '''
                self.World.change_back_to_s() #change back to s
                self.World.Home_Spread(id_d, day) # spread disease
                self.World.Recover() #recovery
                self.World.Intro_New_Thread(day) # intro new disease

                day = day + 1  # update simulation day

                if day % 10 == 0:
                    print("Current Day: ", day)

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