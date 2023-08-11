import random

from src.agent import Agent
from src.parameter import N
from src.parameter import NI


class World(object):
    def __init__(self):
        # Number of Agnets
        self.numberOfAgent = N
        # Generate Agents list
        self.agent = [Agent(self) for i in range(self.numberOfAgent)]

    def __initialize_agents__(self, pop, H, W, S, D):  # population dataset, hhold network, work network, School network,, daycare network
        index_list = []
        id_list = []
        for i in range(self.numberOfAgent):
            index_list.append(i)
            # ID
            self.agent[i].id = str(pop.id[i])
            id_list.append(self.agent[i].id)
            # print(type(self.agent[i].id))
            # age
            self.agent[i].age = int(pop.age[i])

            # status
            self.agent[i].status = 0  # set healthy at the initialization

            # hhold
            self.agent[i].hhold_id = pop.hhold[i]# hhold id
            self.agent[i].hhold_size = H.degree(self.agent[i].id)# hhold size
            self.agent[i].hhold_member = list(H.neighbors(self.agent[i].id))# hhold member

            # work place
            self.agent[i].work_id = pop.wp[i]

            # #get id based on age and workplace ID
            if self.agent[i].age >= 18: #Adults
                if self.agent[i].work_id == self.agent[i].hhold_id:# work from home
                    self.agent[i].work_size = self.agent[i].hhold_size
                    self.agent[i].work_member = self.agent[i].hhold_member
                else:
                    self.agent[i].work_size = W.degree(self.agent[i].id)# work size
                    self.agent[i].work_member = list(W.neighbors(self.agent[i].id))# work member


            elif self.agent[i].age <= 3:# kids go to daycare
                if self.agent[i].work_id == self.agent[i].hhold_id:# stay at home
                    self.agent[i].work_size = self.agent[i].hhold_size
                    self.agent[i].work_member = self.agent[i].hhold_member
                else:# go to daycare
                    self.agent[i].work_size = D.degree(self.agent[i].id)# daycare nw size
                    self.agent[i].work_member = list(D.neighbors(self.agent[i].id))# daycare network member

            elif (self.agent[i].age < 18) and (self.agent[i].age > 3):# kids go to school
                self.agent[i].work_size = S.degree(self.agent[i].id)# school nw size
                self.agent[i].work_member = list(S.neighbors(self.agent[i].id))# school network member

        id_dictionary = dict(zip(id_list, index_list))  # save all agent to dictionary

        # set infected agents (one or more)
        # random choose five agents and set them as infected
        for j in range(NI):
            x = random.choice(range(N))
            self.agent[x].status = 2     # random.randint(1, 2) #change status to infected, ini exposed or infected
            self.agent[x].days = 1       # first day infected
            self.agent[x].thread = 1     # the model starts with the orignial covid thread
            self.agent[x].get_from = 101 #Patiant 0
            self.agent[x].Set_Thread_Info()
            print("Init_agent->The Infected Nodes is ", x, "status", self.agent[x].status, "thread",
                  self.agent[x].thread, "incubation", self.agent[x].incubation, "spread speed",
                  self.agent[x].spread_speed)

        return id_dictionary
    # =================================================================

    def Home_Spread(self, id_dict, DAY):
        # print('-Home Networks Spread')
        for i in range(self.numberOfAgent):
            # 1
            self.agent[i].Get_Infected(DAY)  # change status from 1 to 2
            # 2
            #if (self.agent[i].status == 1) or (self.agent[i].status == 2):
            self.Spread_Home_Network(i, id_dict)#select 1 and 2 spread, then 0 become 1

    def Spread_Home_Network(self, indi, id_dict):
        #print("Home Spread...")
        # print("-2.1Home-", self.agent[indi].id, "'s hhold size", self.agent[indi].hhold_size,"Status", self.agent[indi].status, "Thread:", self.agent[indi].thread, "R0", self.agent[indi].r)
        if (self.agent[indi].status == 1) or (self.agent[indi].status == 2):
            #if self.agent[indi].status == 2: print(self.agent[indi].id, "status", self.agent[indi].status)
            if random.random() < self.agent[indi].spread_speed:
                #print("-2-In Spread_Through Home Network...")
                for member in range(self.agent[indi].hhold_size):  # Loop through the household memebrs
                    a_id = self.agent[indi].hhold_member[member]
                    a_index = id_dict.get(a_id)
                    if (self.agent[a_index].status != 4 and
                        self.agent[a_index].thread != self.agent[indi].thread): # agent not dead and agent thread is not equal to the thread that going to get

                        if (self.agent[a_index].status == 0):  # only s can get infected
                            if self.agent[indi].r > 0:  # check if the indi agent still can spread the disease
                                # print("----Before", self.agent[indi].id, "'s Ro is", self.agent[indi].r)
                                self.agent[indi].r = self.agent[indi].r - 1  # R0 - 1
                                # print("----After", self.agent[indi].id, "'s Ro is", self.agent[indi].r)

                                self.agent[a_index].status = 1
                                self.agent[a_index].days = 1
                                self.agent[a_index].location = 1  # infected at home
                                self.agent[a_index].get_from = self.agent[indi].id
                                self.agent[a_index].where = self.agent[
                                    indi].hhold_id  # get infected home id or loactions
                                self.agent[a_index].thread = self.agent[indi].thread  # set the infected thread
                                # print("--home-spread--", self.agent[a_index].id,
                                # "get infected, thread", self.agent[a_index].thread,
                                # "days", self.agent[a_index].days,
                                # "get exposed from", self.agent[a_index].id,
                                # "at", self.agent[a_index].where)
                                self.agent[a_index].Set_Thread_Info()
        #else:
            #print("no spread")
            # 1 check thread
    # =================================================================

    def Work_Spread(self, id_dict, DAY):
        # print('-Work Networks Spread')
        for i in range(self.numberOfAgent):
            # 1
            self.agent[i].Get_Infected(DAY)  # change status from 1 to 2
            # 2
            #if (self.agent[i].status == 1) or (self.agent[i].status == 2):  # 1 and 2 spread, then 0 become 1
            self.Spread_Work_Network(i, id_dict)

    def Spread_Work_Network(self, indi, id_dict):
        #print("Work Spread...")
        # print("-2.2Work-", self.agent[indi].id, "'s work size", self.agent[indi].work_size,"Status",
        # self.agent[indi].status, "Thread:", self.agent[indi].thread, "R0", self.agent[indi].r)
        if (self.agent[indi].status == 1) or (self.agent[indi].status == 2):
            if random.random() < self.agent[indi].spread_speed:
                #print("-2-In Spread_Through Work Network...")
                for j in range(self.agent[indi].work_size):
                    a_id = self.agent[indi].work_member[j]
                    a_index = id_dict.get(a_id)

                    if (self.agent[a_index].status != 4 and
                        self.agent[indi].thread != self.agent[a_index].thread):  # agent not dead and agent thread is not equal to the thread that going to get
                        #if self.agent[indi].thread == 2:print("thread 2 spread")
                        if (self.agent[a_index].status == 0):  # only s can get infected
                            if self.agent[indi].r > 0:  # check if the indi agent still can spread the disease
                                # print("----Before", self.agent[indi].id, "'s Ro is", self.agent[indi].r)
                                self.agent[indi].r = self.agent[indi].r - 1  # R0 - 1
                                # print("----After", self.agent[indi].id, "'s Ro is", self.agent[indi].r)

                                self.agent[a_index].status = 1
                                self.agent[a_index].days = 1
                                self.agent[a_index].location = 1  # infected at home
                                self.agent[a_index].get_from = self.agent[indi].id
                                self.agent[a_index].where = self.agent[indi].work_id  # get infected home id or loactions
                                self.agent[a_index].thread = self.agent[indi].thread  # set the infected thread
                                # print("--work-spread--", self.agent[a_index].id,
                                # "get infected, thread", self.agent[a_index].thread,
                                # "days", self.agent[a_index].days,
                                # "get exposed from", self.agent[a_index].id,
                                # "at", self.agent[a_index].where)
                                self.agent[a_index].Set_Thread_Info()
    # =================================================================

    def Recover(self):
        for i in range(self.numberOfAgent):
            if (self.agent[i].status == 2) and (self.agent[i].days == self.agent[i].recovery):
                # print(self.agent[i].id, "Recover")
                if random.random() < 0.005:
                    self.agent[i].status = 4  # die
                else:
                    self.agent[i].status = 3  # revover
                    self.agent[i].incubation = 0  # reset incubation
                    self.agent[i].days = 0
                    self.agent[i].recovery_day = 1

    # =================================================================
    def Intro_New_Thread(self, DAY):
        # ramdom select an agent that is not 1 or 2 and assign it with new thread
        '''
            introduce the delta thread on day 60
            introduce the omicorn on day 120
        '''
        if DAY == 70:
            print("change from 1 to 2...")
            for j in range(NI):
                selected = random.choice(range(N))
                #print(selected)
                self.agent[selected].status = 2  #random.randint(1, 2) #change status to infected, ini exposed or infected
                self.agent[selected].days = 1    #first day infected
                self.agent[selected].thread = 2
                self.agent[selected].Set_Thread_Info()
                print("Intro_New_Thread->The Infected Nodes is ", self.agent[selected].id, "status", self.agent[selected].status,
                      "thread", self.agent[selected].thread, "incubation", self.agent[selected].incubation)

            #return id_dict
        #if DAY == 90:
            #print("change from 2 to 3...")
            #for j in range(2):
                #selected = random.choice(range(N))
               #print(selected)
                #self.agent[
                    #selected].status = 2  # random.randint(1, 2) #change status to infected, ini exposed or infected
                #self.agent[selected].days = 1  # first day infected
                #self.agent[selected].thread = 3
                #self.agent[selected].Set_Thread_Info()
                #print("Intro_New_Thread->The Infected Nodes is ", selected, "status", self.agent[selected].status,
                      #"thread", self.agent[selected].thread, "incubation", self.agent[selected].incubation
    # =================================================================

    def change_back_to_s(self):
        for agent in self.agent:
            if agent.recovery_day == 15:
                agent.status = 0 #reset status
                agent.recovery_day = 0 #reset recovery

    def Update_SEIR(self, DAY):
        num_s = 0
        num_e = 0
        num_i = 0
        num_r = 0
        num_d = 0
        T = DAY
        for agent in self.agent:
            if agent.status == 0: #S
                num_s += 1

            if agent.status == 1:#E
                agent.days += 1
                num_e += 1

            if agent.status == 2:#I
                agent.days += 1
                num_i += 1

            if agent.status == 3:#R
                agent.recovery_day += 1
                num_r += 1

            if agent.status == 4:#D
                num_d + 1

        return T, num_s, num_e, num_i, num_r, num_d
    def Update_SEIR_List(self, DAY):
        t2 = []

        S = []

        E = []
        E1 = []
        E2 = []


        I = []
        I1 = []
        I2 = []


        R = []
        R1 = []
        R2 = []

        D = []

        T = DAY
        for i in range(self.numberOfAgent):

            if self.agent[i].status == 0:
                S.append(self.agent[i].id)

            if self.agent[i].status == 1:
                #self.agent[i].days += 1  # Update Days
                #print("update exposed days", self.agent[i].days)

                E.append(self.agent[i].id)
                if self.agent[i].thread == 1:
                    #print("append E t1")
                    E1.append(self.agent[i].id)

                elif self.agent[i].thread == 2:
                    #print("append E t2")
                    E2.append(self.agent[i].id)


            if self.agent[i].status == 2:
                #self.agent[i].days += 1  # Update Days
                #print("update infected days", self.agent[i].days)

                I.append(self.agent[i].id)
                if self.agent[i].thread == 1:
                    #print("append I t1")
                    I1.append(self.agent[i].id)

                elif self.agent[i].thread == 2:
                    #print("append I t2")
                    I2.append(self.agent[i].id)


            if self.agent[i].status == 3:
                R.append(self.agent[i].id)
                if self.agent[i].thread == 1:
                    R1.append(self.agent[i].id)

                elif self.agent[i].thread == 2:
                    R2.append(self.agent[i].id)

            if self.agent[i].status == 4:
                D.append(self.agent[i].id)

        if len(t2) > 0: print("Thread 2", len(t2))
        if T % 10 == 0:
            print("E")
            print(len(E1))
            print(len(E2))
            print("I")
            print(len(I1))
            print(len(I2))
        return T, len(S), len(E), len(E1), len(E2), len(I), len(I1), len(I2), len(R), len(R1), len(R2), len(D)

    # =================================================================
    def Get_Location(self, DAY):
        Home = []
        Work = []
        Daycare = []
        School = []
        T = DAY
        # print(T)
        for i in range(self.numberOfAgent):
            if self.agent[i].status == 2:
                # home
                if (self.agent[i].location == 2) and (self.agent[i].when == DAY):
                    # print("Case 1")
                    Home.append(self.agent[i].id)
                elif (self.agent[i].location == 1) and (self.agent[i].when == DAY):
                    # print("Case 2")
                    # daycare
                    if self.agent[i].age <= 2:
                        # print("Case 2.1")
                        Daycare.append(self.agent[i].id)
                    # school
                    if (self.agent[i].age <= 17) and (self.agent[i].age >= 3):
                        # print("Case 2.2")
                        School.append(self.agent[i].id)
                    # work
                    if self.agent[i].age >= 18:
                        # print("Case 2.3")
                        Work.append(self.agent[i].id)

        return T, len(Home), len(Work), len(Daycare), len(School)

    def track_exposed_history(self, DAY):
        #print("track called")
        times = []
        id = []
        location = []
        from_whom = []

        for i in range(self.numberOfAgent):
            if (self.agent[i].status == 1)and (self.agent[i].days == 1):
                #print("inidi days", self.agent[i].days)
                #if(self.agent[i].days == 1):
                #print("SEIR->Track-History->id", self.agent[i].id)
                times.append(DAY)
                id.append(self.agent[i].id)
                location.append(self.agent[i].where)
                from_whom.append(self.agent[i].get_from)

        return times, id, location, from_whom
