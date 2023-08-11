import random
import matplotlib.pyplot as plt

from src.parameter import INTRO

# Random int generator based on normal distribution
def GenBoundedRandomNormal(meanVal, stdDev, lowerBound, upperBound):
    aRand = random.gauss(meanVal, stdDev)  # could also use: normalvariate()but gauss () is slightly faster.

    while (aRand < lowerBound or aRand > upperBound):
        aRand = random.gauss(meanVal, stdDev)
    return aRand


def plot_SEIR(df):
    print(df.head())
    fig, ax = plt.subplots(figsize=(25, 10))

    # plt.figure(figsize=(25,10))
    plt.xlabel('time $t$', fontsize=20, fontname="Arial")
    plt.ylabel('Population', fontsize=20, fontname="Arial")

    if INTRO == True:
        plt.plot(df.index, df.E1, marker='*', markerfacecolor='gray', markersize= 10, color='yellow', linewidth=2)
        plt.plot(df.index, df.E2, marker='+', markerfacecolor='gray', markersize= 10, color='orange', linewidth=2)

        plt.plot(df.index, df.I1, marker='*', markerfacecolor='gray', markersize=10, color='red', linewidth=2)
        plt.plot(df.index + 1, df.I2, marker='+', markerfacecolor='gray', markersize=10, color='pink', linewidth=2)

        plt.plot(df.index, df.R1, marker='*', markerfacecolor='gray', markersize=10, color='green', linewidth=2)
        plt.plot(df.index + 1, df.R2, marker='+', markerfacecolor='gray', markersize=10, color='springgreen', linewidth=2)

    #if INTRO == False:
        #plt.plot(df.index, df.S, marker='o', markerfacecolor='gray', markersize=2, color='skyblue', linewidth=2)

    #plt.plot(df.index, df.E, marker='o', markerfacecolor='gray', markersize=2, color='yellow', linewidth=2)
        # plt.plot(df.index, df.E1, marker='*', markerfacecolor='gray', markersize= 10, color='yellow', linewidth=2)
        # plt.plot(df.index + 1, df.E2, marker='+', markerfacecolor='gray', markersize= 10, color='orange', linewidth=2)
        # plt.plot(df.index + 1, df.E3, marker='+', markerfacecolor='gray', markersize= 10, color='orange', linewidth=2)

    #plt.plot(df.index, df.I, marker='o', markerfacecolor='gray', markersize=2, color='red', linewidth=2)
        # plt.plot(df.index, df.I1, marker='*', markerfacecolor='gray', markersize=10, color='red', linewidth=2)
        # plt.plot(df.index + 1, df.I2, marker='+', markerfacecolor='gray', markersize=10, color='pink', linewidth=2)
        # plt.plot(df.index + 1, df.I3, marker='+', markerfacecolor='gray', markersize= 10, color='darkred', linewidth=2)

    plt.plot(df.index, df.R, marker='o', markerfacecolor='gray', markersize=2, color='green', linewidth=2)
        # plt.plot(df.index, df.R1, marker='*', markerfacecolor='gray', markersize=10, color='green', linewidth=2)
        # plt.plot(df.index + 1, df.R2, marker='+', markerfacecolor='gray', markersize=10, color='springgreen', linewidth=2)

    plt.plot(df.index, df.D, marker='o', markerfacecolor='gray', markersize=2, color='black', linewidth=2)
        # plt.legend(('Susceptible', 'Exposed', 'Infectious','Recovered', 'Dead'), prop={"size":20}, fancybox=True, framealpha=1, shadow=True,loc = 'upper right', ncol = 5)


    plt.gcf().autofmt_xdate()  # italics of x label
        # plt.savefig('SEIR_WL.png')
    plt.show()