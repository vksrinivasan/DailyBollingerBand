# Author: Vyas K. Srinivasan
# Simulator Code

import numpy as np
import pandas as pd
from PDsymbols import get_symbols
import matplotlib.pyplot as plt
from utils import getListOfStockNames, writeToDisk

from utils import getData
from bollingerBands import getPositions, getBollingerBandIndicator, getBostian, getPositions_bOnly

def getRollingSharpe(np_returns, df_dates):
    # it is just easier to calculate rolling statistics using dataframes
    ls_columns = ['Returns']
    df_total = pd.DataFrame(data=np_returns,index=df_dates,columns=ls_columns)
    np_stdev = df_total.rolling(2520).std().values
    np_mean = df_total.rolling(2520).mean().values

    np_rollingSharpe = (np_mean*np.sqrt(252))/np_stdev
    # pd_plotDF = pd.DataFrame(data=np_rollingSharpe[2520:-1764],
    #                          index=pd.to_datetime(df_dates[2520:-1764],format="%Y%m%d"),
    #                          columns=['Rolling 10y Sharpe'])
    # pd_plotDF.plot()

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
    ls_names = getListOfStockNames(str_data_folder=r"E:\DelistedStockHistory\Clean\Delisted Securities")

    for name in ls_names:

        print("Calculating Results For Name: " + name)

        df_data = getData(str_data_folder=r"E:\DelistedStockHistory\Clean\Delisted Securities", str_ticker=name, str_freq="D")
        np_returns = getReturns(df_data)

        if(np_returns.size == 0):
            continue

        np_bbp = getBollingerBandIndicator(df_data, 20)
        np_vi = getBostian(df_data, 20)
        np_positions = getPositions(np_bbp, np_vi)
        # np_positions = getPositions_bOnly(np_bbp)
        np_stratReturns = calculateReturns(np_positions, np_returns)
        getRollingSharpe(np_stratReturns,df_data['Date'].values[1:])
        cumRet, sharpe, avgRetAnn, volAnn = getResults(np_stratReturns)
        print(" ")

        dict_results = {'Ticker': name,
                        'Returns': np_returns,
                        'Dates': df_data['Date'].values[1:],
                        'CumRet': cumRet,
                        'Sharpe': sharpe,
                        'AvgRetAnn': avgRetAnn,
                        'volAnn': volAnn}

        writeToDisk(dict_results, name, "E:\Results")




if __name__ == "__main__":
    main()
