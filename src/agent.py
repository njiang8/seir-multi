from src.tools import GenBoundedRandomNormal
import random

class Agent(object):
    def __init__(self, World):

        self.id = 0
        self.age = 0

        # hhold
        self.hhold_id = []
        self.hhold_size = []
        self.hhold_member = []

        # work
        self.work_id = []
        self.work_size = []
        self.work_member = []

        # S, 0; E, 1; I, 2; R,3; D,4
        self.status = 0
        self.infected = 0 #if agent infected change to 1
        # Threads
        self.thread = 0  # 1 is orginal; 2 is delta; 3 is omnicorn
        self.r = 0  # R0 of different threads
        self.spread_speed = 0

        # incubation days
        self.incubation = 0
        self.recovery = 0

        # days track
        self.days = 0
        self.recovery_day = 0
        self.location = 0  # if infected in work set 1, if at home set 2
        self.get_from = 0
        self.where = 0 #should be a lat and long
        self.when = 0 #for stat aim
        self.carry = 0

    def Set_Thread_Info(self):
        # if the agent is the first day to get infected then se the incubation and r0
        if (self.status == 1) or (self.status == 2):
            # print("--Ini-- Set Thread")
            if (self.thread == 1) and (self.days == 1):
                # print("First day get Infected")
                # print("---set thread 1.., before set days:", self.days)
                self.incubation = int(GenBoundedRandomNormal(8, 2, 7, 14))  # incubation 7 to 14 days
                self.recovery = int(GenBoundedRandomNormal(7, 2, 4, 14))
                # self.r = 3
                self.r = int(GenBoundedRandomNormal(3, 1, 1, 6))
                self.days = 1
                self.spread_speed = 0.1

            elif (self.thread == 2) and (self.days == 1):
                self.incubation = int(GenBoundedRandomNormal(5, 2, 3, 10))  # incubation 3 to 10 days
                self.recovery = int(GenBoundedRandomNormal(5, 2, 4, 14))
                self.r = int(GenBoundedRandomNormal(5, 1, 1, 9))
                self.days = 1
                self.spread_speed = 0.3

            elif (self.thread == 3) and (self.days == 1):
                self.incubation = int(GenBoundedRandomNormal(5, 2, 3, 10))  # incubation 3 to 10 days
                self.recovery = int(GenBoundedRandomNormal(3, 2, 4, 14))
                self.r = int(GenBoundedRandomNormal(5, 1, 1, 9))
                self.days = 1
                self.spread_speed = 0.6

    def Get_Infected(self, DAY):
        if (self.status == 1) and (self.days == self.incubation):# if E reaches the incubation day
            #print("Get_Infected...")
            self.status = 2
            self.days = 1
            self.when = DAY  # infected day when s change from 1 to 2