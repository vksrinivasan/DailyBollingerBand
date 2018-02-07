# Author: Vyas K. Srinivasan
# Simulator Code

import numpy as np
import pandas as pd

from utils import getData
from bollingerBands import getPredictions

# Helper function to calculate portfolio dollar value
# based on shares held/cash on hand
def calculatePortVal(df_data, index, sPos, sVal):
    return sVal + (sPos*df_data.iloc[index]['Close'])

# Helper function to update position/wealth
def handleTrade(sharesNeeded, df_data, index, sVal):
    closePrice = df_data.iloc[index]['Close']
    tradeDollarAmount = closePrice * sharesNeeded
    if(sharesNeeded > 0):
        sVal = sVal - tradeDollarAmount
    else:
        sVal = sVal + tradeDollarAmount

    return sVal

# Workhorse to actually simulate portfolio size
# sVal: How much cash I start with, will be updated per period
# sPos: How much stock I start with, will be updated per period
def simulatePerformance(df_data, np_decisions, sVal=10000000, sPos=0):
    np_decisions = 100*np_decisions # We need to talk about whether methodology should be capped position sizes
    np_pos = np.zeros((df_data.shape[0]))
    np_pVal = np.zeros((df_data.shape[0]))

    for i in range(0, df_data.shape[0],1):
        if(sPos == np_decisions[i]):
            np_pos[i] = sPos
            np_pVal[i] = calculatePortVal(df_data, i, sPos, sVal)
        else:
            s_needed = np_decisions[i] - sPos
            sVal = handleTrade(s_needed, df_data, i, sVal)
            sPos = np_decisions[i]
            np_pos[i] = sPos
            np_pVal[i] = calculatePortVal(df_data, i, sPos, sVal)

    return np_pVal

def main():
    df_data = getData()
    np_decisions = getPredictions(df_data,20)
    np_pVal = simulatePerformance(df_data, np_decisions)

    for val in np_pVal:
        print val

if __name__ == "__main__":
    main()
