# Author: Vyas K. Srinivasan
# Simulator Code

import numpy as np
import pandas as pd
from utils import getListOfStockNames, writeToDisk

from utils import getData
from bollingerBands import getPositions, getBollingerBandIndicator, getBostian

def getReturns(df_data):
    np_prices = df_data['Close'].values
    np_returns = (np_prices[1:]/np_prices[:-1])-1
    return np_returns

def calculateReturns(np_positions, np_returns):
    return np_positions[:-1]*np_returns[:]

def getResults(np_returns):
    print('Cumulative Return: ' + str((np.cumprod(np_returns+1)-1)[-1]))
    print('Sharpe (Annualized): ' + str(np.sqrt(252)*np.mean(np_returns)/np.std(np_returns,ddof=1)))
    print('Simple Return (Annualized): ' + str(252*np.mean(np_returns)))
    print('Stdev (Annualized): ' + str(252*np.std(np_returns,ddof=1)))

    return (np.cumprod(np_returns+1)-1)[-1], np.sqrt(252)*np.mean(np_returns)/np.std(np_returns,ddof=1), 252*np.mean(np_returns), 252*np.std(np_returns,ddof=1)


def main():
    ls_names = getListOfStockNames()

    for name in ['A']:#ls_names:

        print("Calculating Results For Name: " + name)

        df_data = getData(str_data_folder="D:\ListedStockHistory\Clean\US\NYSE", str_ticker=name, str_freq="D")
        np_returns = getReturns(df_data)
        np_bbp = getBollingerBandIndicator(df_data, 20)
        np_vi = getBostian(df_data, 20)
        np_positions = getPositions(np_bbp, np_vi)
        np_stratReturns = calculateReturns(np_positions, np_returns)
        cumRet, sharpe, avgRetAnn, volAnn = getResults(np_stratReturns)
        print(" ")

        dict_results = {'Ticker': name,
                        'Returns': np_returns,
                        'Dates': df_data['Date'].values[1:],
                        'CumRet': cumRet,
                        'Sharpe': sharpe,
                        'AvgRetAnn': avgRetAnn,
                        'volAnn': volAnn}

        writeToDisk(dict_results, name, "D:\Results")




if __name__ == "__main__":
    main()
